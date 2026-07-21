from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.property.models import Amenity
from apps.property.serializers import AmenitySerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Catalogs'],
    summary="List amenities",
    description="Returns a list of all available property or units amenities.",
    responses=AmenitySerializer(many=True),
)
class AmenityListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()