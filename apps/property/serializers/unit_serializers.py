from rest_framework import serializers

from apps.property.mixins.content_source import ContentSourceMixin
from apps.media.serializers.gallery_serializers.unit_image_serializers import UnitImageCoverSerializer
from apps.property.serializers.bed_serializers import BedSerializer
from apps.property.models import Unit, Amenity


class UnitCreateSerializer(serializers.ModelSerializer):
    amenities = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    beds = BedSerializer(many=True, required=False)
    class Meta:
        model = Unit
        fields = [
            'title',
            'description',
            'status',
            'price_per_night',
            'area',
            'bedrooms',
            'bathrooms',
            'max_guests',
            'room_number',
            'amenities',
            'beds',
        ]



class UnitUpdateSerializer(serializers.ModelSerializer, ContentSourceMixin):
    amenities = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Amenity.objects.all(),
        many=True,
        required=False,
    )
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    beds = BedSerializer(many=True, required=False)
    class Meta:
        model = Unit
        fields = [
            'title',
            'description',
            'status',
            'price_per_night',
            'area',
            'bedrooms',
            'bathrooms',
            'max_guests',
            'room_number',
            'amenities',
            'images',
            'beds',
        ]



class UnitListSerializer(serializers.ModelSerializer, ContentSourceMixin):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cover_image =   serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = [
            'uuid',
            'title',
            'description',
            'price_per_night',
            'area',
            'amenities',
            'max_guests',
            'cover_image',
        ]

    def get_cover_image(self, obj):
        image = obj.images.filter(is_cover=True).first()
        if image:
            return UnitImageCoverSerializer(image, context=self.context).data
        return None


class UnitDetailSerializer(serializers.ModelSerializer, ContentSourceMixin):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    beds = BedSerializer(many=True, read_only=True)
    amenities = serializers.SerializerMethodField()
    class Meta:
        model = Unit
        fields = [
            'uuid',
            'title',
            'description',
            'price_per_night',
            'area',
            'bedrooms',
            'bathrooms',
            'amenities',
            'max_guests',
            'room_number',
            'images',
            'beds',
        ]