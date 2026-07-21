import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.media.models import PropertyImage
from apps.media.tests.factories.property_image_factory import PropertyImageFactory
from apps.media.tests.helper import make_image
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.users.tests.user_factory import UserFactory


def upload_url(property_uuid):
    return reverse('media:property-image-upload', kwargs={'property_uuid': property_uuid})


def delete_url(property_uuid, property_image_uuid):
    return reverse(
        'media:property-image-delete',
        kwargs={'property_uuid': property_uuid, 'property_image_uuid': property_image_uuid},
    )


def cover_url(property_uuid, property_image_uuid):
    return reverse(
        'media:property-image-set-cover',
        kwargs={'property_uuid': property_uuid, 'property_image_uuid': property_image_uuid},
    )


def order_url(property_uuid):
    return reverse('media:property-image-set-order', kwargs={'property_uuid': property_uuid})


@pytest.mark.django_db
class TestPropertyImageUploadAPIView:
    def test_upload_unauthorized(self):
        prop = PropertyFactory()
        client = APIClient()

        response = client.post(upload_url(prop.uuid), data={'images': [make_image()]}, format='multipart')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_upload_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.post(upload_url(prop.uuid), data={'images': [make_image()]}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert PropertyImage.objects.filter(property=prop).count() == 1

    def test_upload_to_foreign_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.post(upload_url(prop.uuid), data={'images': [make_image()]}, format='multipart')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_upload_with_no_images_fails(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.post(upload_url(prop.uuid), data={'images': []}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_invalid_file_type_fails(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        fake_file = SimpleUploadedFile('doc.txt', b'not an image', content_type='text/plain')
        response = client.post(upload_url(prop.uuid), data={'images': [fake_file]}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPropertyImageDeleteAPIView:
    def test_delete_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        image = PropertyImageFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.delete(delete_url(prop.uuid, image.uuid))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not PropertyImage.objects.filter(uuid=image.uuid).exists()

    def test_delete_of_foreign_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)
        image = PropertyImageFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.delete(delete_url(prop.uuid, image.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPropertyImageSetCoverAPIView:
    def test_set_cover_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        image = PropertyImageFactory(property=prop, is_cover=False)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(cover_url(prop.uuid, image.uuid))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        image.refresh_from_db()
        assert image.is_cover is True

    def test_set_cover_unsets_previous_cover(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        old_cover = PropertyImageFactory(property=prop, is_cover=True)
        new_cover = PropertyImageFactory(property=prop, is_cover=False)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(cover_url(prop.uuid, new_cover.uuid))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        old_cover.refresh_from_db()
        new_cover.refresh_from_db()
        assert old_cover.is_cover is False
        assert new_cover.is_cover is True


@pytest.mark.django_db
class TestPropertyImageSetOrderAPIView:
    def test_set_order_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        image_1 = PropertyImageFactory(property=prop, ordering=0)
        image_2 = PropertyImageFactory(property=prop, ordering=1)

        client = APIClient()
        client.force_authenticate(owner)
        payload = [
            {'uuid': str(image_1.uuid), 'ordering': 1},
            {'uuid': str(image_2.uuid), 'ordering': 0},
        ]
        response = client.patch(order_url(prop.uuid), data=payload, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        image_1.refresh_from_db()
        image_2.refresh_from_db()
        assert image_1.ordering == 1
        assert image_2.ordering == 0

    def test_set_order_invalid_payload_fails(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.patch(order_url(prop.uuid), data=[{'ordering': -1}], format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
