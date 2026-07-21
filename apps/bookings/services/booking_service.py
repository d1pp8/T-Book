from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from apps.property.models import Unit

from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus
from apps.bookings.validators import BookingsValidator
from apps.bookings.exceptions import (
    InvalidCancellation,
    BookingStateConflict
)


class BookingService:
    @classmethod
    def create(cls, user, unit: Unit, check_in, check_out, adults: int, children:int = 0, special_request:str = "",) -> Booking:
        with transaction.atomic():
            Unit.objects.select_for_update().get(uuid=unit.uuid)
            BookingsValidator.validate_dates(check_in, check_out)
            BookingsValidator.validate_capacity(unit, adults, children)
            BookingsValidator.validate_availability(unit, check_in, check_out)
            total_price = cls._calculate_total_price(unit, check_in, check_out)
            booking = Booking.objects.create(
                        user=user,
                        unit=unit,
                        check_in=check_in,
                        check_out=check_out,
                        adults=adults,
                        children=children,
                        price_per_night=unit.price_per_night,
                        total_price=total_price,
                        special_request=special_request,
                    )
        return booking

    @classmethod
    def cancel(cls, booking: Booking) -> Booking:

        if not cls._is_cancellation_allowed(booking):
            raise InvalidCancellation()

        return cls._change_status(
            booking,
            new_status=BookingStatus.CANCELLED,
            allowed_statuses=(BookingStatus.PENDING, BookingStatus.CONFIRMED)
        )

    @classmethod
    def reject(cls, booking: Booking) -> Booking:
        return cls._change_status(
            booking,
            new_status=BookingStatus.REJECTED,
            allowed_statuses=(BookingStatus.PENDING,)
        )

    @classmethod
    def confirm(cls, booking: Booking) -> Booking:
        return cls._change_status(
            booking,
            new_status=BookingStatus.CONFIRMED,
            allowed_statuses=(BookingStatus.PENDING,)
        )

    @classmethod
    def complete(cls, booking: Booking) -> Booking:
        if timezone.localdate() < booking.check_out:
            raise BookingStateConflict('The trip is not yet finished; the status cannot be updated.')

        return cls._change_status(
            booking,
            new_status=BookingStatus.COMPLETED,
            allowed_statuses=(BookingStatus.CONFIRMED,)
        )

    @classmethod
    def _calculate_total_price(cls, unit: Unit, check_in, check_out) -> Decimal:
        interval = (check_out - check_in).days
        return interval * unit.price_per_night

    @classmethod
    def _change_status(cls, booking: Booking, new_status, allowed_statuses) -> Booking:
        if booking.status not in allowed_statuses:
            raise BookingStateConflict(f"Cannot change booking status from {booking.status} to {new_status}.")
        booking.status = new_status
        booking.save(update_fields=["status"])
        return booking

    @classmethod
    def _is_cancellation_allowed(cls, booking: Booking) -> bool:
        days_before_check_in = (booking.check_in - timezone.localdate()).days
        return days_before_check_in >= 2