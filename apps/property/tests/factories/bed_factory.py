import factory

from apps.property.tests.factories.unit_factories import UnitFactory
from apps.property.models import Bed

class BedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bed

    unit = factory.SubFactory(UnitFactory)
    bed_type = factory.Iterator([
        Bed.BedType.SINGLE,
        Bed.BedType.DOUBLE,
    ])
    quantity = 1

