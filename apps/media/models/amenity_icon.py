from django.db import models

from apps.media.models import Media
from apps.property.models import Amenity
from apps.common.models import TimeStampedModel, UUIDModel



class AmenityIcon(TimeStampedModel, UUIDModel):

    amenity = models.OneToOneField(
        Amenity,
        on_delete=models.CASCADE,
        related_name='icon',
    )

    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
        related_name='amenity_icon',
    )