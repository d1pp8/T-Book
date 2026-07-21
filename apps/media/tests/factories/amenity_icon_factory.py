import factory

from apps.media.models import AmenityIcon
from apps.media.tests.factories.media_factory import MediaFactory
from apps.property.tests.factories.amenity_factory import AmenityFactory


class AmenityIconFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AmenityIcon

    amenity = factory.SubFactory(AmenityFactory)
    media = factory.SubFactory(MediaFactory)