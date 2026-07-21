from apps.media.models import PropertyImage

from apps.media.serializers.gallery_serializers.gallery_serializers import (
    GalleryImageSerializer,
    GalleryImageUploadSerializer,
    GalleryImageOrderingSerializer,
    GalleryImageCoverSerializer
)

class PropertyImageSerializer(GalleryImageSerializer):
    class Meta(GalleryImageSerializer.Meta):
        model = PropertyImage

class PropertyImageCoverSerializer(GalleryImageCoverSerializer):
    class Meta(GalleryImageCoverSerializer.Meta):
        model = PropertyImage


class PropertyImageUploadSerializer(GalleryImageUploadSerializer):
    pass


class PropertyImageOrderingSerializer(GalleryImageOrderingSerializer):
    pass
