from django.urls import path

from apps.reviews.views import (
    ReviewListCreateAPIView,
    ReviewDetailUpdateDestroyAPIView
)

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view(), name='list-create-review'),
    path('<uuid:review_uuid>/', ReviewDetailUpdateDestroyAPIView.as_view(), name='detail-update-delete-review'),
]