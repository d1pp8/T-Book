import pytest

from apps.listings.selectors import ListingData
from apps.listings.selectors import ListingSelector
from apps.listings.search import ListingSearchParams



from apps.media.tests.factories.amenity_icon_factory import AmenityIconFactory
from apps.media.tests.factories.property_image_factory import PropertyImageFactory

from apps.property.tests.factories.bed_factory import BedFactory
from apps.property.tests.factories.amenity_factory import AmenityFactory
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.unit_factories import UnitFactory

from apps.property.models import Unit


@pytest.mark.django_db
def test_group_by_property():
    unit1 = UnitFactory()
    unit2 = UnitFactory(property=unit1.property)
    unit3 = UnitFactory()

    groups = ListingSelector._group_by_property(
        [unit1, unit2, unit3]
    )

    assert len(groups) == 2
    assert groups[0].property == unit1.property

    assert len(groups[0].units) == 2
    assert groups[1].property == unit3.property
    assert len(groups[1].units) == 1


@pytest.mark.django_db
def test_group_units_by_title():
    first = UnitFactory(title="Standard")
    second = UnitFactory(
        property=first.property,
        title="Standard",
    )

    deluxe = UnitFactory(title='Deluxe')
    groups = ListingSelector._group_units_by_title([first, second, deluxe])

    assert len(groups) == 2
    assert len(groups['Standard']) == 2
    assert len(groups['Deluxe']) == 1


@pytest.mark.django_db
def test_get_single_unit():
    property = PropertyFactory(type='house')
    unit = UnitFactory(property=property)

    data = ListingData(property=property, units=[unit])
    assert ListingSelector._get_single_unit(data) == unit


@pytest.mark.django_db
def test_get_single_unit_hotel():
    property = PropertyFactory(type="hotel")
    unit = UnitFactory(property=property)
    data = ListingData(property=property,units=[unit])

    assert ListingSelector._get_single_unit(data) is None


@pytest.mark.django_db
def test_filter_capacity():
    UnitFactory(max_guests=2)
    UnitFactory(max_guests=4)

    queryset = Unit.objects.all()
    queryset = ListingSelector._filter_capacity(
        queryset=queryset,
        search=ListingSearchParams(
            adults=2,
            children=1,
        ),
    )

    assert queryset.count() == 1
    assert queryset.first().max_guests == 4


@pytest.mark.django_db
def test_build_gallery():
    property = PropertyFactory()
    first = PropertyImageFactory(property=property)
    second = PropertyImageFactory(property=property)
    gallery = ListingSelector._build_gallery(property)

    assert gallery == [first.media.file.url, second.media.file.url]



@pytest.mark.django_db
def test_build_amenities():
    amenity = AmenityFactory(title="Wi-Fi")
    AmenityIconFactory(amenity=amenity)

    dto = ListingSelector._build_amenities([amenity])

    assert len(dto) == 1
    assert dto[0].title == "Wi-Fi"
    assert dto[0].icon is not None



@pytest.mark.django_db
def test_build_beds():

    unit = UnitFactory()
    first = BedFactory(unit=unit, quantity=2)
    second = BedFactory(unit=unit, quantity=1)

    dto = ListingSelector._build_beds([first, second])

    assert len(dto) == 2

    assert dto[0].quantity == 2
    assert dto[1].quantity == 1


@pytest.mark.django_db
def test_build_card():
    property = PropertyFactory()

    first = UnitFactory(
        property=property,
        price_per_night=100,
        max_guests=2,
    )
    second = UnitFactory(
        property=property,
        price_per_night=200,
        max_guests=4,
    )

    data = ListingData(property=property, units=[first, second],)
    dto = ListingSelector._build_card(data)

    assert dto.uuid == property.uuid
    assert dto.price_from == 100
    assert dto.guests_to == 4