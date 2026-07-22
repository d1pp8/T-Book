from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from apps.bookings.mixins import BookingOwnerLookupMixin
from apps.bookings.models import Booking
from apps.bookings.services import BookingService

from apps.bookings.serializers import (
    BookingOwnerDetailSerializer,
    BookingOwnerListSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
import logging

logger = logging.getLogger(__name__)

@extend_schema(
    tags=['Property owner Bookings'],
    summary="All bookings for this property",
    description="The property owner sees all bookings with all statuses.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListAllAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user)

@extend_schema(
    tags=['Property owner Bookings'],
    summary="All active bookings for this property",
    description="The property owner sees active bookings.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListActiveAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).active()

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Confirmed bookings for this property",
    description="The property owner sees all confirmed bookings.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListConfirmedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).confirmed()

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Pending bookings for this property",
    description="The property owner sees all pending bookings.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListPendingAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).pending()

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Cancelled/Rejected bookings for this property",
    description="The property owner sees all cancelled and rejected bookings.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListCancelledOrRejectedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).cancelled_rejected()

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Completed bookings for this property",
    description="The property owner sees all completed bookings.",
    responses=BookingOwnerListSerializer(many=True)
)
class BookingOwnerListCompletedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).completed()

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Property owner Booking details",
    description="""
    Returns detailed information about a booking.
    Accessible only to the owner of the property associated with the booking.
    """,
    responses=BookingOwnerDetailSerializer,
)
class BookingOwnerDetailAPIView(RetrieveAPIView, BookingOwnerLookupMixin):
    serializer_class = BookingOwnerDetailSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'booking_uuid'
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user)


@extend_schema(
    tags=['Property owner Bookings'],
    summary="Confirm booking",
    description="""
Confirm an existing booking.

Confirmation is allowed only:
- for PENDING bookings;

Returns updated booking.
""",
    responses={
        200: BookingOwnerDetailSerializer,
        400: OpenApiResponse(description='Confirm is not allowed'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Booking not found'),
    }
)
class BookingOwnerConfirmAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.confirm(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    tags=['Property owner Bookings'],
    summary="Reject booking",
    description="""
Reject an existing booking.

Reject is allowed only:
- for PENDING bookings;

Returns updated booking.
""",
    responses={
        200: BookingOwnerDetailSerializer,
        400: OpenApiResponse(description='Reject is not allowed'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Booking not found'),
    }
)
class BookingOwnerRejectAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.reject(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Property owner Bookings'],
    summary="Reject booking",
    description="""
Complete an existing booking.

Completion is allowed only:

- for CONFIRMED bookings;
- after the check-out date.

Returns updated booking.
""",
    responses={
        200: BookingOwnerDetailSerializer,
        400: OpenApiResponse(description='Complete is not allowed'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Booking not found'),
    }
)
class BookingOwnerCompleteAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.complete(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)