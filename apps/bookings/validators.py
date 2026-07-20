
from django.utils import timezone
from apps.bookings.services import AvailabilityService

from apps.bookings.exceptions import (
    UnitNotAvailable,
    InvalidBookingDate,
    CapacityExceeded
)

class BookingsValidator:
    @staticmethod
    def validate_dates(check_in, check_out) -> None:
        if check_in < timezone.localdate():
            raise InvalidBookingDate('The check-in date cannot be earlier than today.')
        if check_out <= check_in:
            raise InvalidBookingDate('The departure date cannot be earlier than the arrival date.')

    @staticmethod
    def validate_capacity(unit, adults, children) -> None:
        if adults < 1:
            raise CapacityExceeded('At least one adult is required.')
        if adults + children > unit.max_guests:
            raise CapacityExceeded('Maximum guests exceeded.')

    @staticmethod
    def validate_availability(unit, check_in, check_out) -> None:
        if not AvailabilityService.is_available(unit, check_in, check_out):
            raise UnitNotAvailable()