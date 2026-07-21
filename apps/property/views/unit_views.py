from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from apps.property.mixins.get_property import PropertyLookupMixin
from apps.property.services import UnitService

from apps.property.serializers import (
    UnitCreateSerializer,
    UnitUpdateSerializer,
    UnitListSerializer,
    UnitDetailSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)


@extend_schema_view(
    get=extend_schema(
        tags=['Units'],
        summary="List units",
        description="Returns all units belonging to the specified property owned by the authenticated user.",
        responses=UnitListSerializer(many=True),
    ),
    post=extend_schema(
        tags=['Units'],
        summary="Create unit",
        description=
        """
        Creates a new unit for the specified property.
        
        Requirements:
        
        - the authenticated user must own the property;
        - all required fields must be provided.
        """,
        request=UnitCreateSerializer,
        responses={
            201: UnitDetailSerializer,
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Property not found"),
        },
    ),
)
class UnitListCreateAPIView(ListCreateAPIView, PropertyLookupMixin):

    def get_queryset(self):
        return self.get_property().units.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UnitCreateSerializer
        return UnitListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        unit = UnitService.create_unit(self.get_property(), serializer.validated_data)

        output = UnitDetailSerializer(unit, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

@extend_schema_view(
    get=extend_schema(
        tags=['Units'],
        summary="Unit details",
        description="Returns detailed information about a unit belonging to the specified property.",
        responses=UnitDetailSerializer,
    ),
    put=extend_schema(
        tags=['Units'],
        summary="Replace unit",
        description="Replaces all editable information about the unit.",
        request=UnitUpdateSerializer,
        responses=UnitDetailSerializer,
    ),
    patch=extend_schema(
        tags=['Units'],
        summary="Update unit",
        description="Updates one or more editable fields of the unit.",
        request=UnitUpdateSerializer,
        responses=UnitDetailSerializer,
    ),
    delete=extend_schema(
        tags=['Units'],
        summary="Delete unit",
        description="Deletes a unit belonging to the specified property.",
        responses={
            204: OpenApiResponse(description="Unit deleted successfully."),
            404: OpenApiResponse(description="Unit not found."),
        },
    ),
)
class UnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, PropertyLookupMixin):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'unit_uuid'

    def get_queryset(self):
        return self.get_property().units.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UnitDetailSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return UnitUpdateSerializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        unit = UnitService.update_unit(serializer.instance, serializer.validated_data)
        serializer.instance = unit

    def perform_destroy(self, instance):
        UnitService.delete_unit(instance)


