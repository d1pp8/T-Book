import pytest
from apps.media.models import Media

from apps.media.services.gallery_services.property_image_service import PropertyImageService
from apps.media.tests.helper import make_image
from apps.property.tests.factories.property_factory import PropertyFactory


@pytest.mark.django_db
def test_upload_creates_property_image():
    property = PropertyFactory()
    uploaded_file = make_image()

    image = PropertyImageService.upload(
        owner=property,
        uploaded_file=uploaded_file,
    )

    assert property.images.count() == 1
    assert Media.objects.count() == 1

    assert image.property == property
    assert image.is_cover is True
    assert image.ordering == 0

    assert image.media.original_name == uploaded_file.name
    assert image.media.width == 100
    assert image.media.height == 100



@pytest.mark.django_db
def test_upload_second_image():
    property = PropertyFactory()
    PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image(name="first.jpg"),
    )
    second = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image(name="second.jpg"),
    )

    assert property.images.count() == 2
    second.refresh_from_db()
    assert second.ordering == 1
    assert second.is_cover is False


@pytest.mark.django_db
def test_upload_many():
    property = PropertyFactory()

    images = PropertyImageService.upload_many(
        owner=property,
        uploaded_files=[
            make_image('1.jpg'),
            make_image('2.jpg'),
            make_image('3.jpg'),
        ],
    )

    assert property.images.count() == 3
    assert images[0].ordering == 0
    assert images[1].ordering == 1
    assert images[2].ordering == 2
    assert images[0].is_cover is True


@pytest.mark.django_db
def test_delete_image():
    property = PropertyFactory()
    image = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image(),
    )
    media_id = image.media.id
    PropertyImageService.delete(image)
    assert property.images.count() == 0
    assert not Media.objects.filter(id=media_id).exists()


@pytest.mark.django_db
def test_delete_cover_sets_next_cover():
    property = PropertyFactory()

    first = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image('1.jpg'),
    )
    second = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image('2.jpg'),
    )

    PropertyImageService.delete(first)
    second.refresh_from_db()

    assert second.is_cover is True


@pytest.mark.django_db
def test_set_cover():
    property = PropertyFactory()
    first = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image("1.jpg"),
    )
    second = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image("2.jpg"),
    )

    PropertyImageService.set_cover(second)
    first.refresh_from_db()
    second.refresh_from_db()

    assert first.is_cover is False
    assert second.is_cover is True


@pytest.mark.django_db
def test_reorder():
    property = PropertyFactory()

    first = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image("1.jpg"),
    )
    second = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image("2.jpg"),
    )
    third = PropertyImageService.upload(
        owner=property,
        uploaded_file=make_image("3.jpg"),
    )

    PropertyImageService.reorder(
        owner=property,
        validated_data=[
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
        ],
    )

    first.refresh_from_db()
    second.refresh_from_db()
    third.refresh_from_db()

    assert first.ordering == 2
    assert second.ordering == 0
    assert third.ordering == 1