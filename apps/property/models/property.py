from django.db import models
from django.conf import settings

from apps.common.models import (
    SoftDeleteModel,
    TimeStampedModel,
    UUIDModel
)
from apps.common.mixins import MediaOwnerMixin

class Property(MediaOwnerMixin, TimeStampedModel, SoftDeleteModel, UUIDModel):

    class Type(models.TextChoices):
        HOTEL = 'hotel', 'Hotel'
        HOSTEL = 'hostel', 'Hostel'
        APARTMENT = 'apartment' ,'Apartment'
        VILLA = 'villa', 'Villa'
        HOUSE = 'house', 'House'


    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        UNDER_RENOVATION = 'under_renovation', 'Renovations in progress'

    MEDIA_FOLDER = 'properties'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    type = models.CharField(max_length=20, choices=Type.choices)                                #type: ignore
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)             #type: ignore

    title = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20, blank=True)

    floor = models.PositiveSmallIntegerField(blank=True,null=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    amenities = models.ManyToManyField(
        'Amenity',
        related_name='properties',
        blank=True
    )

    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        editable=False
    )
    review_count = models.PositiveIntegerField(default=0, editable=False)
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        constraints = [
            models.UniqueConstraint(
                fields=['street', 'house_number',  'postal_code', 'floor'],
                name='unique_property_street_house_number_postal_code_floor'
            )
        ]

    @property
    def is_single_unit(self):
        return self.type in (
            self.Type.VILLA,
            self.Type.APARTMENT,
            self.Type.HOUSE
        )

    def __str__(self):
        return self.title