from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from .search import ListingSearchParams
from .selectors import ListingSelector

from .serializers import (
    ListingCardSerializer,
    ListingDetailSerializer,
    ListingSearchSerializer,
)


class ListingListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        filters = request.GET

        search_serializer = ListingSearchSerializer(data=request.GET)
        search_serializer.is_valid(raise_exception=True)
        search = ListingSearchParams(**search_serializer.validated_data)

        cards = ListingSelector.get_list(filters=filters, search=search)
        serializer = ListingCardSerializer(cards, many=True)
        return Response(serializer.data)


class ListingDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, property_uuid):
        filters = request.GET
        search_serializer = ListingSearchSerializer(data=request.GET)
        search_serializer.is_valid(raise_exception=True)
        search = ListingSearchParams(**search_serializer.validated_data)

        dto = ListingSelector.get_detail(property_uuid, search=search, filters=filters)
        serializer = ListingDetailSerializer(dto)
        return Response(serializer.data)