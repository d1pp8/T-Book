from apps.media.models import UnitImage

from apps.media.serializers.gallery_serializers.gallery_serializers import (
    GalleryImageSerializer,
    GalleryImageUploadSerializer,
    GalleryImageOrderingSerializer,
    GalleryImageCoverSerializer
)

class UnitImageSerializer(GalleryImageSerializer):
    class Meta(GalleryImageSerializer.Meta):
        model = UnitImage


class UnitImageCoverSerializer(GalleryImageCoverSerializer):
    class Meta(GalleryImageCoverSerializer.Meta):
        model = UnitImage


class UnitImageUploadSerializer(GalleryImageUploadSerializer):
    pass


class UnitImageOrderingSerializer(GalleryImageOrderingSerializer):
    pass
