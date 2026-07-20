from rest_framework.generics import get_object_or_404

class BookingUserLookupMixin:
    def get_booking(self):
        from apps.bookings.models import Booking
        return get_object_or_404(
            Booking.objects.filter(user=self.request.user),
            uuid=self.kwargs['booking_uuid'],
        )

class BookingOwnerLookupMixin:
    def get_booking(self):
        from apps.bookings.models import Booking
        return get_object_or_404(
            Booking.objects.filter(unit__property__owner=self.request.user),
            uuid=self.kwargs['booking_uuid'],
        )