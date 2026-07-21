from django.db import models

from apps.media.models.media import Media
from apps.property.models import Unit
from apps.common.models import TimeStampedModel, UUIDModel



class UnitImage(TimeStampedModel, UUIDModel):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='images',
    )
    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
        related_name = 'unit_images'
    )

    is_cover = models.BooleanField(default=False)
    ordering = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordering']