from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.property.models import Bed


class BedTypeChoicesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response([{'value': value, 'label': label} for value, label in Bed.BedType.choices])