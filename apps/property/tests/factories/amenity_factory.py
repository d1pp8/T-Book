import factory

from apps.property.models import Amenity

class AmenityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Amenity
    title = factory.Sequence(lambda n: f'Amenity {n}')

