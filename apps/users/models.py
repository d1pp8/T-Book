from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import SoftDeleteModel, TimeStampedModel, UUIDModel
from apps.common.mixins import MediaOwnerMixin

from .managers import UserManager


class User(MediaOwnerMixin, AbstractUser, SoftDeleteModel, TimeStampedModel, UUIDModel):

    class Role(models.TextChoices):
        USER = "user", "User"
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"

    class Sex(models.TextChoices):
        MALE = "m", "Male"
        FEMALE = "f", "Female"
        OTHER = "o", "Other"

    class Citizenship(models.TextChoices):
        UKRAINE = "UA", "Ukraine"
        USA = "US", "United States"
        GERMANY = "DE", "Germany"

    MEDIA_FOLDER = 'avatars'

    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    all_objects = models.Manager()

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    phone = models.CharField(max_length=20,blank=True,)
    birth_date = models.DateField(blank=True,null=True,)

    sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        blank=True,
        null=True,
    )

    citizenship = models.CharField(
        max_length=2,
        choices=Citizenship.choices,
        blank=True,
        null=True,
    )
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email}"