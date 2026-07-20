import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.property.models import Property
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.amenity_factory import AmenityFactory
from apps.users.tests.user_factory import UserFactory


def property_list_url():
    return reverse('property:property-list-create')


def property_detail_url(property_uuid):
    return reverse('property:property-detail-update-delete', kwargs={'property_uuid': property_uuid})


def build_property_payload(**overrides):
    payload = {
        'type': Property.Type.APARTMENT,
        'status': Property.Status.ACTIVE,
        'title': 'Cozy flat in Mitte',
        'description': 'A cozy flat near the center',
        'country': 'Germany',
        'city': 'Berlin',
        'street': 'Alexanderplatz',
        'house_number': '1',
        'postal_code': '10178',
        'floor': 2,
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestPropertyListCreateAPIView:
    def test_list_unauthorized(self):
        client = APIClient()
        response = client.get(property_list_url())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_returns_only_own_properties(self):
        owner = UserFactory()
        another_owner = UserFactory()
        PropertyFactory(owner=owner)
        PropertyFactory(owner=another_owner)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(property_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_empty_for_new_owner(self):
        owner = UserFactory()
        client = APIClient()
        client.force_authenticate(owner)

        response = client.get(property_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_create_property_success(self):
        owner = UserFactory()
        client = APIClient()
        client.force_authenticate(owner)

        payload = build_property_payload()
        response = client.post(property_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == payload['title']
        assert response.data['owner'] == owner.id
        assert Property.objects.filter(owner=owner, title=payload['title']).exists()

    def test_create_property_with_amenities(self):
        owner = UserFactory()
        amenity = AmenityFactory()
        client = APIClient()
        client.force_authenticate(owner)

        payload = build_property_payload(amenities=[str(amenity.uuid)])
        response = client.post(property_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data['amenities']) == 1
        assert response.data['amenities'][0]['uuid'] == str(amenity.uuid)

    def test_create_property_unauthorized(self):
        client = APIClient()
        payload = build_property_payload()

        response = client.post(property_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_property_missing_required_field(self):
        owner = UserFactory()
        client = APIClient()
        client.force_authenticate(owner)

        payload = build_property_payload()
        payload.pop('title')

        response = client.post(property_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'title' in response.data

    def test_create_property_invalid_type_choice(self):
        owner = UserFactory()
        client = APIClient()
        client.force_authenticate(owner)

        payload = build_property_payload(type='castle')
        response = client.post(property_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'type' in response.data


@pytest.mark.django_db
class TestPropertyDetailAPIView:
    def test_retrieve_own_property(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.get(property_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['uuid'] == str(prop.uuid)

    def test_retrieve_other_owners_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(property_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_unauthorized(self):
        prop = PropertyFactory()
        client = APIClient()

        response = client.get(property_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_property_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, title='Old title')
        client = APIClient()
        client.force_authenticate(owner)

        response = client.patch(property_detail_url(prop.uuid), data={'title': 'New title'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        prop.refresh_from_db()
        assert prop.title == 'New title'

    def test_update_other_owners_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner, title='Old title')

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(property_detail_url(prop.uuid), data={'title': 'Hacked'}, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        prop.refresh_from_db()
        assert prop.title == 'Old title'

    def test_delete_property_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        client = APIClient()
        client.force_authenticate(owner)

        response = client.delete(property_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_other_owners_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.delete(property_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND
