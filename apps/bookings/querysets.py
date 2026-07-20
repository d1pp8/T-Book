from django.db import models
from apps.bookings.choices import BookingStatus

class BookingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED,])

    def pending(self):
        return self.filter(status=BookingStatus.PENDING)

    def confirmed(self):
        return self.filter(status=BookingStatus.CONFIRMED)

    def cancelled_rejected(self):
        return self.filter(status__in=[BookingStatus.CANCELLED, BookingStatus.REJECTED])

    def completed(self):
        return self.filter(status=BookingStatus.COMPLETED)

    def for_unit(self, unit):
        return self.filter(unit=unit)

    def overlapping(self, check_in, check_out):
        return self.filter(check_in__lt=check_out,check_out__gt=check_in)

    def for_guest(self, user):
        return self.filter(user=user)

    def for_owner(self, user):
        return self.filter(unit__property__owner=user)

    def with_details(self):
        return self.select_related('unit','unit__property','user')