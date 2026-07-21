import factory
from apps.media.models import Media
from apps.media.tests.helper import make_image


class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Media

    file = factory.LazyFunction(make_image)
    original_name = 'image.jpg'
    mime_type = 'image/jpeg'
    size = factory.LazyAttribute(lambda obj: obj.file.size)
    width = 100
    height = 100