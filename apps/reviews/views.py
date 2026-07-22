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
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

import logging
logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        tags=['Reviews'],
        summary="List reviews",
        description="Returns all reviews created by the authenticated user.",
        responses=ReviewListSerializer(many=True),
    ),
    post=extend_schema(
        tags=['Reviews'],
        summary="Create review",
        description="""
        Creates a review for a completed booking.
        
        Requirements:
        
        - the authenticated user must own the booking;
        - the booking must be completed;
        - only one review is allowed per booking.
        """,
        request=ReviewCreateSerializer,
        responses={
            201: ReviewDetailSerializer,
            400: OpenApiResponse(
                description="Validation error or business rule violation."
            ),
            404: OpenApiResponse(
                description="Booking not found."
            ),
        },
    ),
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


@extend_schema_view(
    get=extend_schema(
        tags=['Reviews'],
        summary="Review details",
        description="Returns detailed information about a review created by the authenticated user.",
        responses=ReviewDetailSerializer,
    ),
    patch=extend_schema(
        tags=['Reviews'],
        summary="Update review",
        description="""
        Updates an existing review.
        
        Only the rating and comment can be modified.
        """,
        request=ReviewUpdateSerializer,
        responses={
            200: ReviewDetailSerializer,
            400: OpenApiResponse(
                description="Validation error."
            ),
            404: OpenApiResponse(
                description="Review not found."
            ),
        },
    ),
    put=extend_schema(
        tags=["Reviews"],
        summary="Replace review",
        description="""
        Replaces the editable review data.
    
        Only the rating and comment can be modified.
        """,
        request=ReviewUpdateSerializer,
        responses={
            200: ReviewDetailSerializer,
            400: OpenApiResponse(
                description="Validation error."
            ),
            404: OpenApiResponse(
                description="Review not found."
            ),
        },
    ),
    delete=extend_schema(
        tags=['Reviews'],
        summary="Delete review",
        description="Deletes a review created by the authenticated user.",
        responses={
            204: OpenApiResponse(
                description="Review deleted successfully."
            ),
            404: OpenApiResponse(
                description="Review not found."
            ),
        },
    ),
)
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
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        review = ReviewService.update(user=request.user, review=review, **serializer.validated_data)

        return Response(ReviewDetailSerializer(review).data, status=status.HTTP_200_OK,)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        ReviewService.delete(user=request.user, review=review,)

        return Response(status=status.HTTP_204_NO_CONTENT)