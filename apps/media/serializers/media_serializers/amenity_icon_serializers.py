from apps.media.models import AmenityIcon

from apps.media.serializers.media_serializers.base_image_serializers import (
    BaseImageUploadSerializer,
    BaseImageSerializer
)

class AmenityIconSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = AmenityIcon


class AmenityIconUploadSerializer(BaseImageUploadSerializer):
    pass
