from django.urls import path
from apps.listings.views import (
    ListingListAPIView,
    ListingDetailAPIView
)

urlpatterns = [
    path('', ListingListAPIView.as_view(), name='listings-list'),
    path('<uuid:property_uuid>/', ListingDetailAPIView.as_view(), name='listings-detail'),
]

