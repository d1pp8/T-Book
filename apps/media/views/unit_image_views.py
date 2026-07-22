from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.property.models import Unit
from apps.media.models import UnitImage
from apps.media.services.gallery_services.unit_image_service import UnitImageService

from apps.media.serializers.gallery_serializers.unit_image_serializers import (
    UnitImageUploadSerializer,
    UnitImageOrderingSerializer
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse
)

import logging

logger = logging.getLogger(__name__)


@extend_schema(
    tags=['Unit Media'],
    summary="Upload unit images",
    description="""
    Uploads one or more images for a unit owned by the authenticated user.
    
    Requirements:
    
    - the authenticated user must own the property;
    - the unit must allow image uploads;
    - uploaded files must be valid images.
    """,
    request=UnitImageUploadSerializer,
        responses={
            201: OpenApiResponse(description="Images uploaded successfully."),
            400: OpenApiResponse(description="Invalid image or validation error."),
            404: OpenApiResponse(description="Unit not found."),
        },
    )
class UnitImageUploadAPIView(APIView):
    def post(self, request, property_uuid, unit_uuid):
        serializer = UnitImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unit = get_object_or_404(
            Unit,
            uuid=unit_uuid,
            property__uuid=property_uuid,
            property__owner=self.request.user
        )

        UnitImageService.validate_images_allowed(unit)
        UnitImageService.upload_many(owner=unit, uploaded_files=serializer.validated_data['images'])

        return Response({'detail': 'Image uploaded successfully.'}, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Unit Media'],
    summary="Delete unit image",
    description="Deletes an image from the unit gallery.",
    responses={
        204: OpenApiResponse(description="Image deleted successfully."),
        404: OpenApiResponse(description="Image not found."),
    },
)
class UnitImageDeleteAPIView(APIView):
    def delete(self, request, property_uuid, unit_uuid, unit_image_uuid):
        unit_image = get_object_or_404(
            UnitImage,
            uuid=unit_image_uuid,
            unit__uuid=unit_uuid,
            unit__property__uuid=property_uuid,
            unit__property__owner=self.request.user
        )

        UnitImageService.validate_images_allowed(unit_image.unit)
        UnitImageService.delete(unit_image)

        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['Unit Media'],
    summary="Set unit cover image",
    description="Marks the selected image as the unit cover image.",
    responses={
        204: OpenApiResponse(description="Cover image updated successfully."),
        404: OpenApiResponse(description="Image not found."),
    },
)
class UnitImageSetCoverAPIView(APIView):
    def patch(self, request, property_uuid, unit_uuid, unit_image_uuid):
        unit_image = get_object_or_404(
            UnitImage,
            uuid=unit_image_uuid,
            unit__uuid=unit_uuid,
            unit__property__uuid=property_uuid,
            unit__property__owner=self.request.user
        )

        UnitImageService.validate_images_allowed(unit_image.unit)
        UnitImageService.set_cover(image=unit_image)

        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    tags=['Unit Media'],
    summary="Reorder unit images",
    description="Updates the display order of images in the unit gallery.",
    request=UnitImageOrderingSerializer(many=True),
    responses={
        204: OpenApiResponse(description="Image order updated successfully."),
        400: OpenApiResponse(description="Validation error."),
        404: OpenApiResponse(description="Unit not found."),
    },
)
class UnitImageSetOrderAPIView(APIView):
    def patch(self, request, property_uuid, unit_uuid):
        serializer = UnitImageOrderingSerializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)

        unit = get_object_or_404(
            Unit,
            uuid=unit_uuid,
            property__uuid=property_uuid,
            property__owner=self.request.user,
        )
        UnitImageService.validate_images_allowed(unit)
        UnitImageService.reorder(owner=unit, validated_data=serializer.validated_data)

        return Response(status=status.HTTP_204_NO_CONTENT)