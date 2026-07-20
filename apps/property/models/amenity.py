from django.db import models

from apps.common.mixins import MediaOwnerMixin
from apps.common.models import TimeStampedModel, UUIDModel, SoftDeleteModel

class Amenity(MediaOwnerMixin, TimeStampedModel, UUIDModel, SoftDeleteModel):
    MEDIA_FOLDER = 'amenities'
    title = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.title
