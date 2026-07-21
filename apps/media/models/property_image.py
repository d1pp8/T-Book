from django.db import models

from apps.media.models.media import Media

from apps.common.models import TimeStampedModel, UUIDModel
from apps.property.models import Property


class PropertyImage(TimeStampedModel, UUIDModel):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
    )
    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
        related_name = 'property_images'
    )

    is_cover = models.BooleanField(default=False)
    ordering = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordering']
