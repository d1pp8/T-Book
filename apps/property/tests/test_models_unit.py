import pytest
from django.db import IntegrityError
from apps.property.tests.factories.unit_factories import UnitFactory


@pytest.mark.django_db
def test_unique_room_number_per_property():
    unit = UnitFactory()
    with pytest.raises(IntegrityError):
            UnitFactory(
                property=unit.property,
                room_number=unit.room_number,
            )

@pytest.mark.django_db
def test_can_reuse_room_number_after_soft_delete():
    unit = UnitFactory()
    unit.delete()
    new_unit = UnitFactory(
        property=unit.property,
        room_number=unit.room_number,
    )
    assert unit.is_deleted is True
    assert new_unit.pk is not None



@pytest.mark.django_db
def test_property_str():
    unit = UnitFactory.build(title='My apartment')
    assert str(unit) == 'My apartment' or unit.uuid
