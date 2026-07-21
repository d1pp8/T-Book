from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from apps.common.pagination import DefaultPagination

from .search import ListingSearchParams
from .selectors import ListingSelector

from .serializers import (
    ListingCardSerializer,
    ListingDetailSerializer,
    ListingSearchSerializer,
)
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=['Listings'],
    summary="Search properties",
    description=
    """
    Public endpoint.
    Returns a list of properties matching the specified search criteria.
    """,
    parameters=[ListingSearchSerializer],
    responses=ListingCardSerializer(many=True)
)
class ListingListAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination

    def get(self, request):
        filters = request.GET
        search_serializer = ListingSearchSerializer(data=request.GET)
        search_serializer.is_valid(raise_exception=True)
        search = ListingSearchParams(**search_serializer.validated_data)

        cards = ListingSelector.get_list(filters=filters, search=search)
        
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(cards, request)

        serializer = ListingCardSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

@extend_schema(
    tags=['Listings'],
    summary="Property details",
    description=
    """
    Public endpoint.
    Returns detailed information about a specific property.
    """,
    parameters=[ListingSearchSerializer],
    responses=ListingDetailSerializer,
)
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