from rest_framework import serializers


class BaseImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        source='media.file',
        read_only=True
    )
    class Meta:
        fields = [
            'uuid',
            'image',
        ]


class BaseImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(), allow_empty=False)