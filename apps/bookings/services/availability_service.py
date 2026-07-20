from apps.bookings.models import Booking


class AvailabilityService:

    @classmethod
    def is_available(cls, unit, check_in, check_out) -> bool:
        return not Booking.objects.active().for_unit(unit=unit).overlapping(check_in, check_out).exists()

    @classmethod
    def available_units(cls, queryset, check_in, check_out):
        busy_units = Booking.objects.active().overlapping(check_in, check_out).values_list('unit_id', flat=True)
        return queryset.exclude(id__in=busy_units)