import pytest
from django.db import IntegrityError
from apps.property.models import Property
from apps.property.tests.factories.property_factory import PropertyFactory




@pytest.mark.parametrize(
    'property_type, expected',
    [
        (Property.Type.HOUSE, True),
        (Property.Type.APARTMENT, True),
        (Property.Type.VILLA, True),
        (Property.Type.HOTEL, False),
        (Property.Type.HOSTEL, False),
    ],
)

def test_property_is_single_unit(property_type, expected):
    prop: Property = PropertyFactory.build(type=property_type)
    assert prop.is_single_unit is expected


@pytest.mark.django_db
def test_property_address_must_be_unique():
    prop = PropertyFactory()
    with pytest.raises(IntegrityError):
        PropertyFactory(
            street=prop.street,
            house_number=prop.house_number,
            postal_code = prop.postal_code,
            floor=prop.floor
        )

@pytest.mark.django_db
def test_property_str():
    prop = PropertyFactory.build(title='My apartment')
    assert str(prop) == 'My apartment'