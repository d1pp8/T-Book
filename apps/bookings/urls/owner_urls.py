from django.urls import path

from apps.bookings.views.owner_views import (
    BookingOwnerListAPIView,
    BookingOwnerDetailAPIView,
    BookingOwnerConfirmAPIView,
    BookingOwnerRejectAPIView,
)

urlpatterns = [
    path('', BookingOwnerListAPIView.as_view(), name='booking-owner-list-create'),
    path('<uuid:booking_uuid>/', BookingOwnerDetailAPIView.as_view(), name='booking-owner-list-bookings'),
    path('<uuid:booking_uuid>/confirm/', BookingOwnerConfirmAPIView.as_view(), name='booking-owner-confim-bookings'),
    path('<uuid:booking_uuid>/reject/', BookingOwnerRejectAPIView.as_view(), name='booking-owner-reject-bookings'),
]