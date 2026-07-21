import pytest
from uuid import uuid4
from apps.listings.search import ListingSearchParams
from apps.listings.selectors import ListingSelector


from rest_framework.exceptions import NotFound

from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.unit_factories import UnitFactory


@pytest.mark.django_db
def test_get_list():
    property = PropertyFactory()

    UnitFactory(property=property, price_per_night=100)

    UnitFactory(property=property, price_per_night=200)

    cards = ListingSelector.get_list(
        filters={},
        search=ListingSearchParams()
    )

    assert len(cards) == 1

    card = cards[0]

    assert card.uuid == property.uuid
    assert card.title == property.title
    assert card.price_from == 100


@pytest.mark.django_db
def test_get_detail_single_property():
    property = PropertyFactory(type='house')

    unit = UnitFactory(property=property,price_per_night=150)

    dto = ListingSelector.get_detail(
        property.uuid,
        search=ListingSearchParams(),
        filters={}
    )

    assert dto.uuid == property.uuid
    assert dto.unit_uuid == unit.uuid
    assert dto.price_per_night == 150
    assert dto.categories == []



@pytest.mark.django_db
def test_get_detail_hotel():
    property = PropertyFactory(type='hotel')
    UnitFactory(property=property, title='Standard', price_per_night=100)

    UnitFactory(property=property, title='Standard', price_per_night=150)

    dto = ListingSelector.get_detail(
        property.uuid,
        search=ListingSearchParams(),
        filters={}
    )

    assert dto.unit_uuid is None
    assert dto.price_per_night is None

    assert len(dto.categories) == 1

    category = dto.categories[0]

    assert category.title == 'Standard'
    assert category.price_from == 100
    assert category.price_to == 150
    assert category.units_available == 2


@pytest.mark.django_db
def test_get_detail_not_found():
    with pytest.raises(NotFound):
        ListingSelector.get_detail(uuid4(),search=ListingSearchParams(),filters={})