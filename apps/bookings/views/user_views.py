from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
)

from apps.bookings.mixins import BookingUserLookupMixin
from apps.bookings.models import Booking
from apps.bookings.services import BookingService

from apps.bookings.serializers import (
    BookingUserCreateSerializer,
    BookingUserDetailSerializer,
    BookingUserListSerializer,
)

class BookingUserListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingUserCreateSerializer
        return BookingUserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = BookingService.create(user=request.user,**serializer.validated_data)

        output = BookingUserDetailSerializer(booking, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


class BookingUserUserDetailAPIView(RetrieveAPIView, BookingUserLookupMixin):
    serializer_class = BookingUserDetailSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'booking_uuid'
    def get_queryset(self):
        return Booking.objects.with_details().for_guest(self.request.user)


class BookingUserUserCancelAPIView(APIView, BookingUserLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.cancel(booking)
        serializer = BookingUserDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)