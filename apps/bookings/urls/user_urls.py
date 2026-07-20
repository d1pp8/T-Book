from django.urls import path

from apps.bookings.views.user_views import (
    BookingUserListCreateAPIView,
    BookingUserUserDetailAPIView,
    BookingUserUserCancelAPIView,

    BookingOwnerListAllAPIView,
    BookingUserListCompletedAPIView,
    BookingUserListCancelledOrRejectedAPIView,

)

app_name = 'bookings'

urlpatterns = [
    path('', BookingUserListCreateAPIView.as_view(), name='booking-user-list-active-create'),

    path('cancelled-rejected/', BookingUserListCancelledOrRejectedAPIView.as_view(), name='booking-user-list-cancelled-rejected'),
    path('completed/', BookingUserListCompletedAPIView.as_view(), name='booking-user-list-completed'),
    path('all/', BookingOwnerListAllAPIView.as_view(), name='booking-user-list-all'),

    path('<uuid:booking_uuid>/', BookingUserUserDetailAPIView.as_view(), name='booking-user-detail'),
    path('<uuid:booking_uuid>/cancel/', BookingUserUserCancelAPIView.as_view(), name='booking-user-cancel'),
]