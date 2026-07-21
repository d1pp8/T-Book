import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.db import IntegrityError
from apps.bookings.exceptions import BookingStateConflict
from apps.bookings.exceptions import InvalidCancellation

from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus
from apps.bookings.services import BookingService
from apps.bookings.tests.booking_factory import BookingFactory

from apps.users.tests.user_factory import UserFactory
from apps.property.tests.factories.unit_factories import UnitFactory


@pytest.mark.django_db
def test_calculate_total_price():
    unit = UnitFactory(price_per_night=Decimal('100'))

    total = BookingService._calculate_total_price(
        unit,
        date.today(),
        date.today() + timedelta(days=3),
    )

    assert total == Decimal('300')




@pytest.mark.django_db
def test_create_booking():
    user = UserFactory()
    unit = UnitFactory(price_per_night=100)

    booking = BookingService.create(
        user=user,
        unit=unit,
        check_in=date.today() + timedelta(days=5),
        check_out=date.today() + timedelta(days=8),
        adults=2,
    )

    assert Booking.objects.count() == 1

    assert booking.user == user
    assert booking.unit == unit
    assert booking.total_price == 300
    assert booking.price_per_night == 100


@pytest.mark.django_db
def test_confirm_booking():
    booking = BookingFactory()
    BookingService.confirm(booking)
    booking.refresh_from_db()

    assert booking.status == BookingStatus.CONFIRMED


@pytest.mark.django_db
def test_reject_booking():
    booking = BookingFactory()
    BookingService.reject(booking)
    booking.refresh_from_db()

    assert booking.status == BookingStatus.REJECTED


@pytest.mark.django_db
def test_cancel_booking():
    booking = BookingFactory(
        status=BookingStatus.CONFIRMED,
        check_in=date.today() + timedelta(days=5),
        check_out=date.today() + timedelta(days=8),
    )
    BookingService.cancel(booking)

    assert booking.status == BookingStatus.CANCELLED


@pytest.mark.django_db
def test_complete_before_trip():
    booking = BookingFactory(
        status=BookingStatus.CONFIRMED,
        check_out=date.today() + timedelta(days=2),
    )

    with pytest.raises(BookingStateConflict):
        BookingService.complete(booking)


@pytest.mark.django_db
def test_cancel_too_late():
    booking = BookingFactory(
        status=BookingStatus.CONFIRMED,
        check_in=date.today() + timedelta(days=1),
    )
    with pytest.raises(InvalidCancellation):
        BookingService.cancel(booking)


@pytest.mark.django_db
def test_confirm_completed_booking():
    booking = BookingFactory(
        status=BookingStatus.COMPLETED,
    )

    with pytest.raises(BookingStateConflict):
        BookingService.confirm(booking)