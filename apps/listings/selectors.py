from rest_framework.exceptions import NotFound
from dataclasses import dataclass
from uuid import UUID

from django.db.models import QuerySet
from apps.reviews.models import Review
from apps.property.models import Property, Unit
from apps.bookings.services import AvailabilityService
from apps.common.mixins import MediaOwnerMixin

from apps.listings.filters import ListingFilter
from apps.listings.search import ListingSearchParams


from apps.listings.dto import (
    ListingCardDTO,
    ListingDetailDTO,
    OwnerDTO,
    AmenityDTO,
    AddressDTO,
    RoomCategoryDTO,
    ReviewDTO,
    BedDTO
)


@dataclass(slots=True)
class ListingData:
    property: Property
    units: QuerySet[Unit]


class ListingSelector:
    @classmethod
    def get_list(cls, filters, search: ListingSearchParams) -> list[ListingCardDTO]:
        queryset = cls._apply_filters(queryset=cls._get_queryset(), filters=filters, search=search)
        groups = cls._group_by_property(queryset)
        return [cls._build_card(data) for data in groups]


    @classmethod
    def get_detail(cls, property_uuid: UUID, search: ListingSearchParams, filters) -> ListingDetailDTO:
        data = cls._get_listing_data(property_uuid)
        data.units = cls._apply_filters(queryset=data.units, filters=filters, search=search)
        if search.check_in and search.check_out:
            data.units = AvailabilityService.available_units(
                queryset=data.units,
                check_in=search.check_in,
                check_out=search.check_out
            )
        return cls._build_detail(data)


    @classmethod
    def _build_card(cls, data: ListingData) -> ListingCardDTO:
        return ListingCardDTO(
            uuid=data.property.uuid,
            type=data.property.type,

            title=data.property.title,
            description=data.property.description,

            cover_image=cls._get_cover_image(data.property),

            country=data.property.country,
            city=data.property.city,

            rating=data.property.rating,
            review_count=data.property.review_count,

            price_from=min(unit.price_per_night for unit in data.units),
            guests_to=max(unit.max_guests for unit in data.units),
            beds=max(sum(bed.quantity for bed in unit.beds.all()) for unit in data.units),
        )

    @classmethod
    def _build_detail(cls, data: ListingData) -> ListingDetailDTO:
        unit = cls._get_single_unit(data)
        return ListingDetailDTO(
            uuid=data.property.uuid,
            owner=cls._build_owner(data.property.owner),
            type=data.property.type,
            title=data.property.title,
            description=data.property.description,

            amenities=cls._build_amenities(data.property.amenities.all()),
            address=cls._build_address(data.property),
            gallery=cls._build_gallery(data.property),

            rating=data.property.rating,
            review_count=data.property.review_count,
            reviews = cls._build_reviews(data.property.reviews.all()),

            unit_uuid=unit.uuid if unit else None,
            price_per_night=unit.price_per_night if unit else None,
            area=unit.area if unit else None,
            bedrooms=unit.bedrooms if unit else None,
            bathrooms=unit.bathrooms if unit else None,
            max_guests=unit.max_guests if unit else None,
            beds=cls._build_beds(unit.beds.all()) if unit else None,

            categories=[] if unit else cls._build_categories(data.units),


        )

    @classmethod
    def _get_queryset(cls) -> QuerySet[Unit]:
        return (
            Unit.objects
            .filter(status=Unit.Status.AVAILABLE, property__status=Property.Status.ACTIVE)
            .select_related('property')
            .prefetch_related('property__images__media', 'beds')
        )

    @classmethod
    def _get_listing_data(cls, property_uuid) -> ListingData:
        try:
            property_obj = (Property.objects
            .select_related('owner')
            .prefetch_related(
                'images__media',
                'units',
                'units__images__media',
                'units__amenities',
                'reviews__user',
                'amenities',
                'amenities__icon__media',
                'units__amenities__icon__media',
                'units__beds',
            )
            .get(uuid=property_uuid, status=Property.Status.ACTIVE,))
        except Property.DoesNotExist:
            raise NotFound('Property not found.')
        return ListingData(property=property_obj, units=(property_obj.units.all()))

    @classmethod
    def _get_cover_image(cls, obj: Property | Unit) -> str | None:
        for image in obj.images.all():
            if image.is_cover:
                return image.media.file.url
        return None


    @classmethod
    def _group_by_property(cls, units: QuerySet[Unit]) -> list[ListingData]:
        groups = {}
        for unit in units:
            if unit.property not in groups:
                groups[unit.property] = ListingData(property=unit.property, units=[])
            groups[unit.property].units.append(unit)
        return list(groups.values())


    @classmethod
    def _group_units_by_title(cls, units: QuerySet[Unit]) -> dict:
        groups = {}
        for unit in units:
            if unit.title not in groups:
                groups[unit.title] = []
            groups[unit.title].append(unit)
        return groups


    @classmethod
    def _get_single_unit(cls, data: ListingData) -> Unit | None:
        if data.property.is_single_unit:
            return data.units[0]
        return None


    @classmethod
    def _build_categories(cls, units: QuerySet[Unit]) -> list[RoomCategoryDTO]:
        groups = cls._group_units_by_title(units)
        categories = []
        for title, units in groups.items():

            prices = [unit.price_per_night for unit in units]
            areas = [unit.area for unit in units]
            guests = [unit.max_guests for unit in units]
            representative = min(units, key=lambda unit: unit.price_per_night)

            categories.append(
                RoomCategoryDTO(
                    unit_uuid= representative.uuid,
                    title=title,
                    description=representative.description,
                    gallery=cls._build_gallery(representative),
                    amenities=cls._build_amenities(representative.amenities.all()),
                    price_from=min(prices),
                    price_to=max(prices),
                    area_from=min(areas),
                    area_to=max(areas),
                    guests_from=min(guests),
                    guests_to=max(guests),
                    units_available=len(units),
                    beds=cls._build_beds(representative.beds.all()),
                )
            )
        return categories


    @classmethod
    def _build_owner(cls,owner) -> OwnerDTO:
        return OwnerDTO(name=owner.get_full_name(), avatar=None)

    @classmethod
    def _build_address(cls, prop: Property) -> AddressDTO:
        return AddressDTO(
            country=prop.country,
            city=prop.city,
            street=prop.street,
            house_number=prop.house_number,
            postal_code=prop.postal_code,
        )
    @classmethod
    def _build_gallery(cls, media_owner: MediaOwnerMixin) -> list[str]:
        return [image.media.file.url for image in media_owner.images.all()]

    @classmethod
    def _build_amenities(cls, amenities):
        return [
            AmenityDTO(
                title=a.title,
                icon=a.icon.media.file.url if getattr(a, 'icon', None) else None,
            )
            for a in amenities
        ]

    @classmethod
    def _build_beds(cls, beds):
        return [BedDTO(type=bed.bed_type, quantity=bed.quantity) for bed in beds]

    @classmethod
    def _build_reviews(cls, reviews: QuerySet[Review]) -> list[ReviewDTO]:
        return [ReviewDTO(
            uuid=review.uuid,
            user=review.user.get_full_name(),
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
        )
            for review in reviews
        ]

    @classmethod
    def _apply_filters(cls, queryset, filters, search: ListingSearchParams):
        queryset = ListingFilter(filters, queryset=queryset).qs
        queryset = cls._filter_capacity(queryset=queryset, search=search)
        queryset = cls._filter_availability(queryset=queryset,search=search)
        return queryset

    @classmethod
    def _filter_availability(cls, queryset, search: ListingSearchParams):
        if not search.check_in or not search.check_out:
            return queryset
        return AvailabilityService.available_units(queryset=queryset, check_in=search.check_in, check_out=search.check_out)

    @classmethod
    def _filter_capacity(cls, queryset, search: ListingSearchParams):
        if search.adults is None:
            return queryset
        guests = search.adults + (search.children or 0)
        return queryset.filter(max_guests__gte=guests)