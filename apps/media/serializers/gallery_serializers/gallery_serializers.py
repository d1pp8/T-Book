from rest_framework import serializers

class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        source='media.file',
        read_only=True,
        help_text='Image URL.'
    )
    class Meta:
        fields = [
            'uuid',
            'image',
            'is_cover',
            'ordering'
        ]


class GalleryImageCoverSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        source='media.file',
        read_only=True
    )
    class Meta:
        fields = [
          'image',
        ]



class GalleryImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False,
        help_text='One or more image files.'
    )


class GalleryImageOrderingSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(help_text='Image UUID.')
    ordering = serializers.IntegerField(
        min_value=0,
        help_text='New image position.'
    )