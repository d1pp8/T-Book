import factory
from apps.media.models import PropertyImage
from apps.media.tests.factories.media_factory import MediaFactory
from apps.property.tests.factories.property_factory import PropertyFactory

class PropertyImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PropertyImage

    property = factory.SubFactory(PropertyFactory)
    media = factory.SubFactory(MediaFactory)

    is_cover = False
    ordering = factory.Sequence(lambda n: n)