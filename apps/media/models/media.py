from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class Media(TimeStampedModel, UUIDModel):

    file = models.ImageField()
    original_name = models.CharField(max_length=255)
    mime_type =  models.CharField(max_length=100)
    size = models.PositiveBigIntegerField()
    width =  models.PositiveIntegerField()
    height =  models.PositiveIntegerField()


    