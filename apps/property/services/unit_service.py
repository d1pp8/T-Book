from rest_framework.exceptions import ValidationError

from django.db import transaction


from apps.property.models import (
    Property,
    Unit,
    Bed
)


class UnitService:
    @staticmethod
    def create_unit(property: Property, validated_data: dict) -> Unit:
        with transaction.atomic():
            if property.is_single_unit and property.units.exists():
                raise ValidationError('Single-unit properties can only have one unit.')

            amenities = validated_data.pop("amenities", [])
            beds = validated_data.pop("beds", [])
            if property.is_single_unit and amenities:
                raise ValidationError('For single-unit properties amenities are set on the property, not the unit.')

            unit = Unit.objects.create(property=property, **validated_data)
            unit.amenities.set(amenities)
            Bed.objects.bulk_create([Bed(unit=unit, **bed) for bed in beds])
            return unit


    @staticmethod
    def update_unit(unit, validated_data):
        with transaction.atomic():
            amenities = validated_data.pop('amenities', None)
            beds = validated_data.pop('beds', None)
            if unit.property.is_single_unit and amenities:
                raise ValidationError('For single-unit properties amenities are set on the property, not the unit.')

            for field, value in validated_data.items():
                setattr(unit, field, value)
            unit.save()

            if amenities is not None:
                unit.amenities.set(amenities)

            if beds is not None:
                for bed in unit.beds.all():
                    bed.hard_delete()
                Bed.objects.bulk_create([Bed(unit=unit, **bed) for bed in beds])
            return unit


    @staticmethod
    def delete_unit(unit):
        if unit.bookings.exists():
            raise ValidationError(...)
        unit.delete()
        
        Unit.deleted_objects.filter(property=unit.property, room_number=unit.room_number,).hard_delete()
