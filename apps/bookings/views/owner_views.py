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


class BookingOwnerListAllAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user)

class BookingOwnerListActiveAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).active()

class BookingOwnerListConfirmedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).confirmed()

class BookingOwnerListPendingAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).pending()

class BookingOwnerListCancelledOrRejectedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).cancelled_rejected()

class BookingOwnerListCompletedAPIView(ListAPIView):
    serializer_class = BookingOwnerListSerializer
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user).completed()


class BookingOwnerDetailAPIView(RetrieveAPIView, BookingOwnerLookupMixin):
    serializer_class = BookingOwnerDetailSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'booking_uuid'
    def get_queryset(self):
        return Booking.objects.with_details().for_owner(self.request.user)


class BookingOwnerConfirmAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.confirm(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingOwnerRejectAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.reject(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingOwnerCompleteAPIView(APIView, BookingOwnerLookupMixin):
    def patch(self, request, booking_uuid):
        booking = self.get_booking()
        booking = BookingService.complete(booking)
        serializer = BookingOwnerDetailSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)