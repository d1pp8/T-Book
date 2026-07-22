from django.urls import path

from apps.bookings.views.owner_views import (
    BookingOwnerListActiveAPIView,

    BookingOwnerListAllAPIView,
    BookingOwnerListConfirmedAPIView,
    BookingOwnerListPendingAPIView,
    BookingOwnerListCancelledOrRejectedAPIView,
    BookingOwnerListCompletedAPIView,

    BookingOwnerDetailAPIView,
    BookingOwnerConfirmAPIView,
    BookingOwnerRejectAPIView,
    BookingOwnerCompleteAPIView
)
app_name = 'bookings-owner'


urlpatterns = [

    path('', BookingOwnerListActiveAPIView.as_view(), name='booking-owner-list-active'),

    path('pending/', BookingOwnerListPendingAPIView.as_view(), name='booking-owner-list-pending'),
    path('confirmed/', BookingOwnerListConfirmedAPIView.as_view(), name='booking-owner-list-confirmed'),
    path('cancelled-rejected/', BookingOwnerListCancelledOrRejectedAPIView.as_view(), name='booking-owner-list-cancelled-rejected'),
    path('completed/', BookingOwnerListCompletedAPIView.as_view(), name='booking-owner-list-completed'),
    path('all/', BookingOwnerListAllAPIView.as_view(), name='booking-owner-list-all'),


    path('<uuid:booking_uuid>/', BookingOwnerDetailAPIView.as_view(), name='booking-owner-detail-bookings'),
    path('<uuid:booking_uuid>/confirm/', BookingOwnerConfirmAPIView.as_view(), name='booking-owner-confirm-bookings'),
    path('<uuid:booking_uuid>/reject/', BookingOwnerRejectAPIView.as_view(), name='booking-owner-reject-bookings'),
    path('<uuid:booking_uuid>/complete/', BookingOwnerCompleteAPIView.as_view(), name='booking-owner-complete-bookings'),
]