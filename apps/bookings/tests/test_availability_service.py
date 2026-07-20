import pytest
from datetime import date, timedelta

from apps.bookings.services import AvailabilityService
from apps.bookings.tests.booking_factory import BookingFactory
from apps.property.tests.factories.unit_factories import UnitFactory


@pytest.mark.django_db
def test_is_available():
    unit = UnitFactory()

    BookingFactory(
        unit=unit,
        check_in=date.today() + timedelta(days=5),
        check_out=date.today() + timedelta(days=10),
    )

    assert (
        AvailabilityService.is_available(
            unit,
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3),
        )
        is True
    )

@pytest.mark.django_db
def test_available_units():
    busy = UnitFactory()
    free = UnitFactory()

    BookingFactory(
        unit=busy,
        check_in=date.today() + timedelta(days=5),
        check_out=date.today() + timedelta(days=10),
    )

    queryset = AvailabilityService.available_units(
        queryset=busy.__class__.objects.all(),
        check_in=date.today() + timedelta(days=7),
        check_out=date.today() + timedelta(days=8),
    )

    assert list(queryset) == [free]