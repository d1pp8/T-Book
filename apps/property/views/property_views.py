from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.property.serializers.property_serializers import(
    PropertyDetailSerializer,
    PropertyCreateSerializer,
    PropertyListSerializer,
    PropertyUpdateSerializer,
)

from apps.property.models import Property


class PropertyListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PropertyCreateSerializer
        return PropertyListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prop = serializer.save(owner=request.user)
        output = PropertyDetailSerializer(prop, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


class PropertyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'property_uuid'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PropertyDetailSerializer

        if self.request.method in ('PUT', 'PATCH'):
            return PropertyUpdateSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PropertyUpdateSerializer(
            instance,
            data=request.data,
            partial=partial,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = PropertyDetailSerializer(instance,context=self.get_serializer_context(),)
        return Response(response_serializer.data)