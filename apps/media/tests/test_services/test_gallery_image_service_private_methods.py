import pytest

from apps.media.tests.helper import make_image
from uuid import uuid4
from apps.media.models import Media

from apps.media.tests.factories.property_image_factory import PropertyImageFactory
from apps.property.tests.factories.property_factory import PropertyFactory



@pytest.mark.django_db
def test_extract_metadata():
    uploaded_file = make_image(name='photo.png')
    metadata = PropertyImageService._extract_metadata(uploaded_file)

    assert metadata['original_name'] == uploaded_file.name
    assert metadata['mime_type'] == uploaded_file.content_type
    assert metadata['size'] == uploaded_file.size
    assert metadata['width'] == 100
    assert metadata['height'] == 100
    assert uploaded_file.tell() == 0


def test_build_upload_path():
    owner = PropertyFactory.build()
    media = Media(uuid=uuid4())
    uploaded_file = make_image(name='photo.jpg')
    path = PropertyImageService._build_upload_path(
        owner=owner,
        media=media,
        uploaded_file=uploaded_file,
    )
    assert path == (
        f'{owner.MEDIA_FOLDER}/'
        f'{owner.uuid}/'
        f'{media.uuid}.jpg'
    )



@pytest.mark.django_db
def test_get_next_ordering_empty():
    property = PropertyFactory()
    assert PropertyImageService._get_next_ordering(property) == 0

@pytest.mark.django_db
def test_is_first_image():
    property = PropertyFactory()
    property_image_factory = PropertyImageFactory
    assert PropertyImageService._is_first_image(property) is True


@pytest.mark.django_db
def test_is_not_first_image():
    property = PropertyFactory()
    PropertyImageFactory(property=property)
    assert PropertyImageService._is_first_image(property) is False

@pytest.mark.django_db
def test_get_next_ordering():
    property = PropertyFactory()
    property_image_factory = PropertyImageFactory
    property_image_factory(property=property, ordering=0)
    property_image_factory(property=property, ordering=1)
    property_image_factory(property=property, ordering=2)

    assert PropertyImageService._get_next_ordering(property) == 3


@pytest.mark.django_db
def test_set_cover():
    property = PropertyFactory()
    property_image_factory = PropertyImageFactory

    first = property_image_factory(property=property, is_cover=True,)
    second = property_image_factory(property=property,is_cover=False,)
    PropertyImageService._set_cover(image=second,images=property.images.all(),)

    first.refresh_from_db()
    second.refresh_from_db()

    assert first.is_cover is False
    assert second.is_cover is True



@pytest.mark.django_db
def test_set_next_cover():
    property = PropertyFactory()
    property_image_factory = PropertyImageFactory
    first = property_image_factory(property=property, ordering=0, is_cover=True)
    second = property_image_factory(property=property, ordering=1, is_cover=False)
    property_image_factory(property=property, ordering=2, is_cover=False)

    PropertyImageService._set_next_cover(property, first)
    second.refresh_from_db()

    assert second.is_cover is True


from apps.media.services.gallery_services.property_image_service import (
    PropertyImageService,
)


def test_set_new_order():
    property_image_factory = PropertyImageFactory
    first = property_image_factory.build(ordering=0)
    second = property_image_factory.build(ordering=1)
    third = property_image_factory.build(ordering=2)

    images = [first, second, third]

    validated_data = [
        {
            "uuid": first.uuid,
            "ordering": 2,
        },
        {
            "uuid": second.uuid,
            "ordering": 0,
        },
        {
            "uuid": third.uuid,
            "ordering": 1,
        },
    ]

    reordered = PropertyImageService._set_new_order(images,validated_data)

    assert reordered[0].ordering == 2
    assert reordered[1].ordering == 0
    assert reordered[2].ordering == 1