import pytest
from apps.property.models import Bed
from apps.property.tests.factories.unit_factories import UnitFactory


@pytest.mark.django_db
def test_bed_str():
    unit = UnitFactory()
    bed = Bed.objects.create(
        unit=unit,
        bed_type=Bed.BedType.KING,
        quantity=2
    )
    assert str(bed) == 'king x 2'