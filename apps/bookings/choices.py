from django.db import models


class BookingStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    COMPLETED = 'completed', 'Completed'
    REJECTED = 'rejected', 'Rejected'


class BookingGuestType(models.TextChoices):
    ADULT = 'adult', 'Adult'
    CHILD = 'child', 'Child'
