import pytest

from apps.bookings.tests.booking_factory import BookingFactory


@pytest.mark.django_db
def test_booking_str():
    booking = BookingFactory()
    assert str(booking) == (f'{booking.unit.title} - {booking.check_in}-{booking.check_out}')