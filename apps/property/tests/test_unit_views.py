import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.property.models import Property, Unit
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.unit_factories import UnitFactory
from apps.users.tests.user_factory import UserFactory


def unit_list_url(property_uuid):
    return reverse('property:unit-list-create', kwargs={'property_uuid': property_uuid})


def unit_detail_url(property_uuid, unit_uuid):
    return reverse(
        'property:unit-detail-update-delete',
        kwargs={'property_uuid': property_uuid, 'unit_uuid': unit_uuid},
    )


def build_unit_payload(**overrides):
    payload = {
        'title': 'Deluxe room',
        'description': 'A spacious room',
        'status': Unit.Status.AVAILABLE,
        'price_per_night': '150.00',
        'area': 30,
        'bedrooms': 1,
        'bathrooms': 1,
        'max_guests': 3,
        'room_number': '201',
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestUnitListCreateAPIView:
    def test_list_units_of_own_property(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)
        UnitFactory(property=prop)
        UnitFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(unit_list_url(prop.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_list_units_of_other_owners_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner, type=Property.Type.HOTEL)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(unit_list_url(prop.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_units_unauthorized(self):
        prop = PropertyFactory(type=Property.Type.HOTEL)
        client = APIClient()

        response = client.get(unit_list_url(prop.uuid))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_unit_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)

        client = APIClient()
        client.force_authenticate(owner)
        payload = build_unit_payload()

        response = client.post(unit_list_url(prop.uuid), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Unit.objects.filter(property=prop, room_number='201').exists()

    def test_create_unit_with_beds(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)

        client = APIClient()
        client.force_authenticate(owner)
        payload = build_unit_payload(beds=[{'bed_type': 'double', 'quantity': 2}])

        response = client.post(unit_list_url(prop.uuid), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        unit = Unit.objects.get(property=prop, room_number='201')
        assert unit.beds.count() == 1
        assert unit.beds.first().quantity == 2

    def test_create_second_unit_for_single_unit_property_fails(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.APARTMENT)
        UnitFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        payload = build_unit_payload(room_number='999')

        response = client.post(unit_list_url(prop.uuid), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_unit_invalid_price(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)

        client = APIClient()
        client.force_authenticate(owner)
        payload = build_unit_payload(price_per_night='not-a-number')

        response = client.post(unit_list_url(prop.uuid), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'price_per_night' in response.data


@pytest.mark.django_db
class TestUnitDetailAPIView:
    def test_retrieve_unit(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop, price_per_night=Decimal('120.00'))

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(unit_detail_url(prop.uuid, unit.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['uuid'] == str(unit.uuid)

    def test_retrieve_unit_of_another_owner_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(unit_detail_url(prop.uuid, unit.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_unit_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop, price_per_night=Decimal('100.00'))

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(
            unit_detail_url(prop.uuid, unit.uuid),
            data={'price_per_night': '175.50'},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        unit.refresh_from_db()
        assert unit.price_per_night == Decimal('175.50')

    def test_delete_unit_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.delete(unit_detail_url(prop.uuid, unit.uuid))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Unit.objects.filter(uuid=unit.uuid).exists()

    def test_delete_unit_with_active_bookings_fails(self):
        from apps.bookings.tests.booking_factory import BookingFactory

        owner = UserFactory()
        prop = PropertyFactory(owner=owner, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop)
        BookingFactory(unit=unit)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.delete(unit_detail_url(prop.uuid, unit.uuid))

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCatalogViews:
    def test_amenities_list_is_public(self):
        from apps.property.tests.factories.amenity_factory import AmenityFactory

        AmenityFactory()
        AmenityFactory()
        client = APIClient()

        response = client.get(reverse('property:amenities-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_bed_types_choices_is_public(self):
        client = APIClient()

        response = client.get(reverse('property:bed-types'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
