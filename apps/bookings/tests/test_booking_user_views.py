import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookings.choices import BookingStatus
from apps.bookings.models import Booking
from apps.bookings.tests.booking_factory import BookingFactory
from apps.property.tests.factories.unit_factories import UnitFactory
from apps.users.tests.user_factory import UserFactory


def booking_list_url():
    return reverse('bookings-user:booking-user-list-active-create')


def booking_detail_url(booking_uuid):
    return reverse('bookings-user:booking-user-detail', kwargs={'booking_uuid': booking_uuid})


def booking_cancel_url(booking_uuid):
    return reverse('bookings-user:booking-user-cancel', kwargs={'booking_uuid': booking_uuid})


def build_booking_payload(unit, **overrides):
    payload = {
        'unit': str(unit.uuid),
        'check_in': (date.today() + timedelta(days=10)).isoformat(),
        'check_out': (date.today() + timedelta(days=15)).isoformat(),
        'adults': 2,
        'children': 0,
    }
    payload.update(overrides)
    return payload


@pytest.mark.django_db
class TestBookingUserListCreateAPIView:
    def test_list_unauthorized(self):
        client = APIClient()
        response = client.get(booking_list_url())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_returns_only_own_bookings(self):
        user = UserFactory()
        another_user = UserFactory()
        BookingFactory(user=user)
        BookingFactory(user=another_user)

        client = APIClient()
        client.force_authenticate(user)
        response = client.get(booking_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_create_booking_success(self):
        user = UserFactory()
        unit = UnitFactory(price_per_night=100, max_guests=4)

        client = APIClient()
        client.force_authenticate(user)
        payload = build_booking_payload(unit)

        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        booking = Booking.objects.get(user=user, unit=unit)
        assert booking.status == BookingStatus.PENDING
        assert booking.total_price == 500  # 5 nights * 100

    def test_create_booking_unauthorized(self):
        unit = UnitFactory()
        client = APIClient()

        response = client.post(booking_list_url(), data=build_booking_payload(unit), format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_booking_with_past_check_in_fails(self):
        user = UserFactory()
        unit = UnitFactory()

        client = APIClient()
        client.force_authenticate(user)
        payload = build_booking_payload(
            unit,
            check_in=(date.today() - timedelta(days=1)).isoformat(),
        )

        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_booking_check_out_before_check_in_fails(self):
        user = UserFactory()
        unit = UnitFactory()

        client = APIClient()
        client.force_authenticate(user)
        payload = build_booking_payload(
            unit,
            check_in=(date.today() + timedelta(days=10)).isoformat(),
            check_out=(date.today() + timedelta(days=5)).isoformat(),
        )

        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_booking_capacity_exceeded_fails(self):
        user = UserFactory()
        unit = UnitFactory(max_guests=2)

        client = APIClient()
        client.force_authenticate(user)
        payload = build_booking_payload(unit, adults=3, children=0)

        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_booking_for_unavailable_unit_fails(self):
        user = UserFactory()
        unit = UnitFactory(max_guests=4)
        BookingFactory(
            unit=unit,
            status=BookingStatus.CONFIRMED,
            check_in=date.today() + timedelta(days=10),
            check_out=date.today() + timedelta(days=15),
        )

        client = APIClient()
        client.force_authenticate(user)
        payload = build_booking_payload(unit)

        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_booking_missing_unit_fails(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user)

        payload = {
            'check_in': (date.today() + timedelta(days=10)).isoformat(),
            'check_out': (date.today() + timedelta(days=15)).isoformat(),
            'adults': 1,
            'children': 0,
        }
        response = client.post(booking_list_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'unit' in response.data


@pytest.mark.django_db
class TestBookingUserDetailAPIView:
    def test_retrieve_own_booking(self):
        user = UserFactory()
        booking = BookingFactory(user=user)

        client = APIClient()
        client.force_authenticate(user)
        response = client.get(booking_detail_url(booking.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['uuid'] == str(booking.uuid)

    def test_retrieve_another_users_booking_returns_404(self):
        user = UserFactory()
        another_user = UserFactory()
        booking = BookingFactory(user=another_user)

        client = APIClient()
        client.force_authenticate(user)
        response = client.get(booking_detail_url(booking.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestBookingUserCancelAPIView:
    def test_cancel_booking_success(self):
        user = UserFactory()
        booking = BookingFactory(
            user=user,
            status=BookingStatus.PENDING,
            check_in=date.today() + timedelta(days=10),
            check_out=date.today() + timedelta(days=15),
        )

        client = APIClient()
        client.force_authenticate(user)
        response = client.patch(booking_cancel_url(booking.uuid))

        assert response.status_code == status.HTTP_200_OK
        booking.refresh_from_db()
        assert booking.status == BookingStatus.CANCELLED

    def test_cancel_booking_too_close_to_check_in_fails(self):
        user = UserFactory()
        booking = BookingFactory(
            user=user,
            status=BookingStatus.PENDING,
            check_in=date.today(),
            check_out=date.today() + timedelta(days=5),
        )

        client = APIClient()
        client.force_authenticate(user)
        response = client.patch(booking_cancel_url(booking.uuid))

        assert response.status_code == status.HTTP_409_CONFLICT
        booking.refresh_from_db()
        assert booking.status == BookingStatus.PENDING

    def test_cancel_already_cancelled_booking_fails(self):
        user = UserFactory()
        booking = BookingFactory(
            user=user,
            status=BookingStatus.CANCELLED,
            check_in=date.today() + timedelta(days=10),
            check_out=date.today() + timedelta(days=15),
        )

        client = APIClient()
        client.force_authenticate(user)
        response = client.patch(booking_cancel_url(booking.uuid))

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_cancel_another_users_booking_returns_404(self):
        user = UserFactory()
        another_user = UserFactory()
        booking = BookingFactory(user=another_user, status=BookingStatus.PENDING)

        client = APIClient()
        client.force_authenticate(user)
        response = client.patch(booking_cancel_url(booking.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND