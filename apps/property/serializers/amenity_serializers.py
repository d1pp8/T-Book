from rest_framework import serializers

from apps.property.models import Amenity
from apps.media.serializers.media_serializers.amenity_icon_serializers import AmenityIconSerializer


class AmenitySerializer(serializers.ModelSerializer):
    icon = AmenityIconSerializer(read_only=True)

    class Meta:
        model = Amenity
        fields = (
            "uuid",
            "title",
            "icon",
        )


class AmenityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "title",
        )