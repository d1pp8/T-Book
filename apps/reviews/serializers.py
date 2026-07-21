from rest_framework import serializers

from apps.bookings.models import Booking
from apps.property.models import Property
from apps.reviews.models import Review



class ReviewCreateSerializer(serializers.Serializer):
    booking = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Booking.objects.all(),
        help_text = 'UUID of the completed booking.'
    )
    rating = serializers.IntegerField(
        min_value=1,
        max_value=10,
        help_text='Rating from 1 to 10.'
    )
    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Optional review comment.'
    )


class ReviewUpdateSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=10)
    comment = serializers.CharField(required=False, allow_blank=True)


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    booking_uuid = serializers.UUIDField(source='booking.uuid')
    property_title = serializers.CharField(source='property.title')
    class Meta:
        model = Review
        fields = [
            'uuid',
            'user',
            'booking_uuid',
            'property_title',
            'created_at',
            'rating',
            'comment'
        ]


class ReviewPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'uuid',
            'title',
            'type',
        ]


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    booking_uuid = serializers.CharField(source='booking.uuid', read_only=True)
    property = ReviewPropertySerializer(read_only=True)
    class Meta:
        model = Review
        fields = [
            'uuid',
            'user',
            'property',
            'booking_uuid',
            'rating',
            'comment',
            'created_at',
        ]