from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from apps.common.models import (
    TimeStampedModel,
    UUIDModel,
)
from apps.bookings.models import Booking
from apps.property.models import Property


class Review(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)
                    ]
    )
    comment = models.TextField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.property.title} ({self.rating}/10)'
