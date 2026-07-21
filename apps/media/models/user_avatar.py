from django.db import models
from apps.common.models import TimeStampedModel, UUIDModel

from django.conf import settings

from .media import Media

class UserAvatar(TimeStampedModel, UUIDModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    media = models.OneToOneField(
        Media,
        on_delete=models.CASCADE,
    )
