from django.db import models
from apps.bookings.models import Booking
from apps.bookings.choices import BookingGuestType

class BookingGuest(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='guests'
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    type = models.CharField(
        max_length=10,
        choices=BookingGuestType.choices,
        default=BookingGuestType.ADULT
    )
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    class Meta:
        verbose_name = 'BookingGuest'
        verbose_name_plural = 'BookingGuests'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'