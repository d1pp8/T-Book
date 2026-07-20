from django.db import models
from .querysets import BookingQuerySet


class BookingManager(models.Manager.from_queryset(BookingQuerySet)):
    pass