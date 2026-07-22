from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    ListAPIView
)

from apps.bookings.mixins import BookingUserLookupMixin
from apps.bookings.models import Booking
from apps.bookings.services import BookingService

from apps.bookings.serializers import (
    BookingUserCreateSerializer,
    BookingUserDetailSerializer,
    BookingUserListSerializer,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

import logging

logger = logging.getLogger(__name__)


class BookingUserListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user).active()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingUserCreateSerializer
        return BookingUserListSerializer

    @extend_schema(
        tags=['Bookings'],
        summary="List active bookings",
        description="Returns all pending and confirmed bookings belonging to the authenticated user.",
        responses=BookingUserListSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Bookings'],
        summary="Create booking",
        description="""
    Creates a new booking.

    Business rules:
    - authentication required;
    - booking dates must be valid;
    - unit capacity must not be exceeded;
    - booking dates must not overlap existing bookings;
    - booking is created with PENDING status.
    """,
        request=BookingUserCreateSerializer,
        responses={
            201: BookingUserDetailSerializer,
            400: OpenApiResponse(description="Validation error"),
            401: OpenApiResponse(description="Authentication required"),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = BookingService.create(user=request.user,**serializer.validated_data)

        output = BookingUserDetailSerializer(booking, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    tags=['Bookings'],
    summary="All bookings",
    description="Returns all pending,confirmed,completed,cancelled,rejected bookings belonging to the authenticated user.",
    responses=BookingUserListSerializer(many=True)
)
class BookingOwnerListAllAPIView(ListAPIView):
    serializer_class = BookingUserListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user)

@extend_schema(
    tags=['Bookings'],
    summary="Completed bookings",
    description="Returns completed bookings of authenticated user.",
    responses=BookingUserListSerializer(many=True)
)
class BookingUserListCompletedAPIView(ListAPIView):
    serializer_class = BookingUserListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user).completed()

@extend_schema(
    tags=['Bookings'],
    summary="Cancelled or rejected bookings",
    description="Returns all cancelled and rejected bookings belonging to the authenticated user.",
    responses=BookingUserListSerializer(many=True)
)
class BookingUserListCancelledOrRejectedAPIView(ListAPIView):
    serializer_class = BookingUserListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user).cancelled_rejected()




@extend_schema(
    tags=["Bookings"],
    summary="Booking details",
    description="Only the user who created the booking can access this endpoint.",
    responses=BookingUserDetailSerializer,
)
class BookingUserDetailAPIView(RetrieveAPIView, BookingUserLookupMixin):
    serializer_class = BookingUserDetailSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'booking_uuid'
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user)


@extend_schema(
    tags=["Bookings"],
    summary="Cancel booking",
    description="""
Cancels an existing booking.

Cancellation is allowed only:

- for PENDING or CONFIRMED bookings;
- at least 2 days before check-in.

Returns updated booking.
""",
    responses={
        200: BookingUserDetailSerializer,
        400: OpenApiResponse(description='Cancellation is not allowed'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Booking not found'),
    }
)
class BookingUserCancelAPIView(APIView, BookingUserLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.cancel(booking)
        serializer = BookingUserDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
