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


