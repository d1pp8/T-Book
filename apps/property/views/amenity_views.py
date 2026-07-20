from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.property.models import Amenity
from apps.property.serializers import AmenitySerializer


class AmenityListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()