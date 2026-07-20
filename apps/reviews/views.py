from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)

from apps.reviews.models import Review
from apps.reviews.services import ReviewService


from apps.reviews.serializers import (
    ReviewCreateSerializer,
    ReviewListSerializer,
    ReviewDetailSerializer,
    ReviewUpdateSerializer
)

class ReviewListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Review.objects.select_related('user', 'property', 'booking').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = ReviewService.create(user=request.user, **serializer.validated_data)
        output = ReviewDetailSerializer(review, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)

        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewDetailUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "uuid"
    lookup_url_kwarg = "review_uuid"

    def get_queryset(self):
        return (Review.objects
                .select_related("user", "property", "booking")
                .filter(user=self.request.user)
                )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ReviewUpdateSerializer
        return ReviewDetailSerializer

    def update(self, request, *args, **kwargs):
        review = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = ReviewService.update(user=request.user, review=review, **serializer.validated_data)

        return Response(ReviewDetailSerializer(review).data, status=status.HTTP_200_OK,)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        ReviewService.delete(user=request.user, review=review,)

        return Response(status=status.HTTP_204_NO_CONTENT)