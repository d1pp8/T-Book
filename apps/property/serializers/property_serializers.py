from rest_framework import serializers

from apps.property.models import Property, Amenity
from apps.media.serializers.gallery_serializers import(
    PropertyImageSerializer,
    PropertyImageCoverSerializer
)
from apps.property.serializers.bed_serializers import BedSerializer
from apps.property.serializers.amenity_serializers import AmenitySerializer


class PropertyCreateSerializer(serializers.ModelSerializer):
    amenities = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    class Meta:
        model = Property
        fields = [
            'type',
            'status',
            'title',
            'description',
            'country',
            'city',
            'street',
            'house_number',
            'postal_code',
            'floor',
            'latitude',
            'longitude',
            'amenities',
        ]


class PropertyListSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    # available_units = serializers.SerializerMethodField() For statistic ToDo
    class Meta:
        model = Property
        fields = [
            'uuid',
            'type',
            'title',
            'status',
            'country',
            'city',
            'street',
            'house_number',
            'rating',
            'cover_image'
        ]

    def get_cover_image(self, obj):
        image = obj.images.filter(is_cover=True).first()
        if image:
            return PropertyImageCoverSerializer(image, context=self.context).data
        return None




class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True,read_only=True)

    unit = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = [
            'uuid',
            'owner',
            'type',
            'status',
            'title',
            'description',
            'country',
            'city',
            'street',
            'house_number',
            'postal_code',
            'floor',
            'latitude',
            'longitude',
            'amenities',
            'rating',
            'images',
            'unit',
        ]

    def get_unit(self, obj):
        if not obj.is_single_unit:
            return None
        unit = obj.units.first()
        if not unit:
            return None
        return {
            'uuid': unit.uuid,
            'status': unit.status,
            'price_per_night': unit.price_per_night,
            'area': unit.area,
            'bedrooms': unit.bedrooms,
            'bathrooms': unit.bathrooms,
            'max_guests': unit.max_guests,
            'beds': BedSerializer(unit.beds.all(), many=True).data,
        }


class PropertyUpdateSerializer(serializers.ModelSerializer):
    amenities = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    class Meta:
        model = Property
        fields = [
            'status',
            'title',
            'description',
            'country',
            'city',
            'street',
            'house_number',
            'postal_code',
            'floor',
            'latitude',
            'longitude',
            'amenities',
        ]