from django.db import models
from apps.common.models import TimeStampedModel, SoftDeleteModel, UUIDModel
from apps.common.mixins import MediaOwnerMixin
from django.core.validators import MaxValueValidator

from apps.bookings.choices import BookingStatus
from apps.property.exceptions import UnitHasActiveBookings

from apps.property.models.property import Property

class Unit(MediaOwnerMixin, TimeStampedModel, SoftDeleteModel, UUIDModel):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        NOT_AVAILABLE = 'not_available', 'Not available'
        UNDER_MAINTENANCE = 'under_maintenance', 'Under Maintenance'

    MEDIA_FOLDER = 'units'

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='units'
    )

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,  # type: ignore
        default=Status.AVAILABLE
    )

    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)

    area = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000),])
    bedrooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10),])
    bathrooms = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10),])

    amenities = models.ManyToManyField(
        'Amenity',
        related_name='units',
        blank=True
    )

    max_guests = models.PositiveSmallIntegerField(validators=[MaxValueValidator(15)],)
    room_number = models.CharField(max_length=30, null=True, blank = True)
    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        constraints = [
            models.UniqueConstraint(
                fields=['property', 'room_number'],
                condition=models.Q(is_deleted=False),
                name='unique_room_number_per_property'
            )
        ]

    def delete(self, *args, **kwargs):
        from apps.bookings.models import Booking

        has_active = Booking.objects.filter(
            unit=self,
            status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED],
        ).exists()
        if has_active:
            raise UnitHasActiveBookings("The unit cannot be deleted — there are active bookings.")
        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.title or f"Unit {self.uuid}"