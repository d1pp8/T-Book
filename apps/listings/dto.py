from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True)
class AddressDTO:
    country: str
    city: str
    street: str
    house_number: str
    postal_code: str


@dataclass(slots=True)
class OwnerDTO:
    name: str
    avatar: str | None


@dataclass(slots=True)
class AmenityDTO:
    title: str
    icon: str | None

@dataclass(slots=True)
class BedDTO:
    type: str
    quantity: int


@dataclass(slots=True)
class ReviewDTO:
    uuid: UUID
    user: str
    rating: int
    comment: str
    created_at: datetime


@dataclass(slots=True)
class RoomCategoryDTO:
    unit_uuid: UUID | None
    title: str
    description: str
    amenities: list[AmenityDTO] | None
    gallery: list[str] | None
    price_from: Decimal
    price_to: Decimal
    area_from: int
    area_to: int
    guests_from: int
    guests_to: int
    units_available: int
    beds: list[BedDTO]


@dataclass(slots=True)
class ListingCardDTO:
    uuid: UUID
    type: str
    title: str
    description: str
    cover_image: str | None
    country: str
    city: str
    rating: Decimal
    review_count: int
    price_from: Decimal
    guests_to: int
    beds: int

@dataclass(slots=True)
class ListingDetailDTO:
    # Property
    uuid: UUID
    owner: OwnerDTO
    type: str
    title: str
    description: str
    amenities: list[AmenityDTO] | None
    address: AddressDTO
    gallery: list[str]

    #Rating
    rating: Decimal
    review_count: int
    reviews: list[ReviewDTO]

    #Single unit
    unit_uuid: UUID | None
    price_per_night: Decimal | None
    area: int | None
    bedrooms: int | None
    bathrooms: int | None
    max_guests: int | None
    beds: list[BedDTO]

    #Hotels only
    categories: list[RoomCategoryDTO]




