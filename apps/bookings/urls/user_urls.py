from django.urls import path

from apps.bookings.views.user_views import (
    BookingUserListCreateAPIView,
    BookingUserUserDetailAPIView,
    BookingUserUserCancelAPIView
)

app_name = 'bookings'

urlpatterns = [
    path('', BookingUserListCreateAPIView.as_view(), name="booking-user-list-create"),
    path('<uuid:booking_uuid>/', BookingUserUserDetailAPIView.as_view(), name="booking-user-detail"),
    path('<uuid:booking_uuid>/cancel/', BookingUserUserCancelAPIView.as_view(), name="booking-user-cancel"),
]