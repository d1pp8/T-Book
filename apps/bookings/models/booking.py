from django.db import models
from django.conf import settings

from apps.property.models import Unit
from apps.common.models import (
    UUIDModel,
    TimeStampedModel,
    SoftDeleteModel
)

from apps.bookings.choices import BookingStatus
from apps.bookings.managers import BookingManager

class Booking(UUIDModel, TimeStampedModel, SoftDeleteModel):

    objects = BookingManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )

    adults = models.PositiveSmallIntegerField(default=1)
    children = models.PositiveSmallIntegerField(default=0)

    is_for_self = models.BooleanField(default=True)

    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    special_request = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(check_out__gt=models.F('check_in')),
                name='booking_check_out_after_check_in'
            ),
            models.CheckConstraint(
                condition=models.Q(adults__gte=1) & models.Q(children__gte=0),
                name='minimum_quantity_of_people'
            )
        ]

    def __str__(self):
        return f"{self.unit.title} - {self.check_in}-{self.check_out}"