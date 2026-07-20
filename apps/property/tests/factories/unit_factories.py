import factory
from decimal import Decimal

from apps.property.models import Unit
from apps.property.tests.factories.property_factory import PropertyFactory

class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Unit

    property = factory.SubFactory(PropertyFactory)
    price_per_night = Decimal('100')
    area = 25
    bedrooms = 1
    bathrooms = 1
    max_guests = 2
    room_number = factory.Sequence(lambda n: f'10{n}')