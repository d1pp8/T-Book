from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.common.models import TimeStampedModel, SoftDeleteModel, UUIDModel
from apps.property.models.unit import Unit

class Bed(TimeStampedModel, SoftDeleteModel, UUIDModel):
    class BedType(models.TextChoices):
        SINGLE = 'single', 'Single'
        DOUBLE = 'double', 'Double'
        QUEEN = 'queen', 'Queen'
        KING = 'king', 'King'
        CALIFORNIA_KING = 'california_king', 'California King'
        BUNK_BED = 'bunk_bed', 'Bunk bed'
        SOFA = 'sofa', 'Sofa'
        PULL_OUT_SOFA = 'pull_out_sofa', 'Pull-out sofa'
        FUTON = 'futon', 'Futon'
        ADJUSTABLE_BED = 'adjustable_bed', 'Adjustable bed'

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name = 'beds'
    )

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    bed_type = models.CharField(
        max_length=30,
        choices=BedType.choices,                                                 #type: ignore
        default=BedType.SINGLE
    )

    def __str__(self):
        return f'{self.bed_type} x {self.quantity}'



