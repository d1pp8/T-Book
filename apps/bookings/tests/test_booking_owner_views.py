import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookings.choices import BookingStatus
from apps.bookings.tests.booking_factory import BookingFactory
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.unit_factories import UnitFactory
from apps.users.tests.user_factory import UserFactory


def booking_owner_list_url():
    return reverse('booking-owner-list-create')


def booking_owner_detail_url(booking_uuid):
    return reverse('booking-owner-list-bookings', kwargs={'booking_uuid': booking_uuid})


def booking_owner_confirm_url(booking_uuid):
    return reverse('booking-owner-confim-bookings', kwargs={'booking_uuid': booking_uuid})


def booking_owner_reject_url(booking_uuid):
    return reverse('booking-owner-reject-bookings', kwargs={'booking_uuid': booking_uuid})


@pytest.mark.django_db
class TestBookingOwnerListAPIView:
    def test_list_unauthorized(self):
        client = APIClient()
        response = client.get(booking_owner_list_url())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_returns_only_bookings_of_owned_properties(self):
        owner = UserFactory()
        another_owner = UserFactory()
        own_property = PropertyFactory(owner=owner)
        own_unit = UnitFactory(property=own_property)
        foreign_property = PropertyFactory(owner=another_owner)
        foreign_unit = UnitFactory(property=foreign_property)

        BookingFactory(unit=own_unit)
        BookingFactory(unit=foreign_unit)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(booking_owner_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_includes_guest_info(self):
        owner = UserFactory()
        guest = UserFactory(first_name='John', last_name='Doe')
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        BookingFactory(unit=unit, user=guest)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(booking_owner_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['user']['email'] == guest.email


@pytest.mark.django_db
class TestBookingOwnerDetailAPIView:
    def test_retrieve_booking_of_owned_property(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(booking_owner_detail_url(booking.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['uuid'] == str(booking.uuid)

    def test_retrieve_booking_of_foreign_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.get(booking_owner_detail_url(booking.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookingOwnerConfirmAPIView:
    def test_confirm_pending_booking_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit, status=BookingStatus.PENDING)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(booking_owner_confirm_url(booking.uuid))

        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.status == BookingStatus.CONFIRMED

    def test_confirm_already_confirmed_booking_fails(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit, status=BookingStatus.CONFIRMED)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(booking_owner_confirm_url(booking.uuid))

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_confirm_booking_of_foreign_property_returns_404(self):
        owner = UserFactory()
        another_owner = UserFactory()
        prop = PropertyFactory(owner=another_owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit, status=BookingStatus.PENDING)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(booking_owner_confirm_url(booking.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookingOwnerRejectAPIView:
    def test_reject_pending_booking_success(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit, status=BookingStatus.PENDING)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(booking_owner_reject_url(booking.uuid))

        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.status == BookingStatus.REJECTED

    def test_reject_confirmed_booking_fails(self):
        owner = UserFactory()
        prop = PropertyFactory(owner=owner)
        unit = UnitFactory(property=prop)
        booking = BookingFactory(unit=unit, status=BookingStatus.CONFIRMED)

        client = APIClient()
        client.force_authenticate(owner)
        response = client.patch(booking_owner_reject_url(booking.uuid))

        assert response.status_code == status.HTTP_409_CONFLICT
