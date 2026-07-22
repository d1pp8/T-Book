from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.property.models import Property
from apps.media.models import PropertyImage

from apps.media.services.gallery_services.property_image_service import PropertyImageService
from apps.media.serializers.gallery_serializers.property_image_serializers import (
    PropertyImageUploadSerializer,
    PropertyImageOrderingSerializer
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
import logging

logger = logging.getLogger(__name__)

@extend_schema(
    tags=['Property Media'],
    summary="Upload property images",
    description=
    """
    Uploads one or more images for a property owned by the authenticated user.
    Requirements:

    - supported image format (png, jpg);
    - maximum allowed file size (5 MB);
    - valid image file.
    """,
    request=PropertyImageUploadSerializer,
)
class PropertyImageUploadAPIView(APIView):
    def post(self, request, property_uuid):
        serializer = PropertyImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        property = get_object_or_404(Property,uuid=property_uuid,owner=self.request.user)
        PropertyImageService.upload_many(owner=property, uploaded_files=serializer.validated_data['images'])

        return Response({'detail': 'Image uploaded successfully.'}, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Property Media'],
    summary="Delete property images",
    description="Deletes an image from the property's gallery.",
    responses={
        204: OpenApiResponse(
            description="Image deleted successfully."
        ),
        404: OpenApiResponse(
            description="Image not found."
        ),
    }
)
class PropertyImageDeleteAPIView(APIView):
    def delete(self, request, property_uuid, property_image_uuid):
        property_image = get_object_or_404(
            PropertyImage,
            uuid=property_image_uuid,
            property__uuid=property_uuid,
            property__owner=self.request.user
        )

        PropertyImageService.delete(image=property_image)
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['Property Media'],
    summary="Set property cover image",
    description="Marks the selected image as the property's cover image.",
)
class PropertyImageSetCoverAPIView(APIView):
    def patch(self, request, property_uuid, property_image_uuid):
        property_image = get_object_or_404(
            PropertyImage,
            uuid=property_image_uuid,
            property__uuid=property_uuid,
            property__owner=self.request.user
        )
        PropertyImageService.set_cover(image=property_image)

        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['Property Media'],
    summary="Reorder property images",
    description="Updates the display order of property gallery images.",
    request=PropertyImageOrderingSerializer(many=True),

)
class PropertyImageSetOrderAPIView(APIView):
    def patch(self, request, property_uuid):
        serializer = PropertyImageOrderingSerializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)

        property = get_object_or_404(
            Property,
            uuid=property_uuid,
            owner=self.request.user
        )
        PropertyImageService.reorder(owner=property, validated_data=serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)