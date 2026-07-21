from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.property.models import Bed
from apps.property.serializers.bed_serializers import ChoiceSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Catalogs'],
    summary="List bed types",
    description="Returns all available bed type choices.",
    responses=ChoiceSerializer(many=True),
)
class BedTypeChoicesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response([{'value': value, 'label': label} for value, label in Bed.BedType.choices])