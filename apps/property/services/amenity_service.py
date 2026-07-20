from apps.property.models import Amenity

class AmenityService:
    @staticmethod
    def create(**validated_data):
        return Amenity.objects.create(**validated_data)

    @staticmethod
    def update(amenity, **validated_data):
        for field, value in validated_data.items():
            setattr(amenity, field, value)
        amenity.save()
        return amenity

    @staticmethod
    def delete(amenity):
        amenity.delete()