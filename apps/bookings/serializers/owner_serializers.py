from rest_framework import serializers
from apps.users.models import User
from apps.bookings.models import Booking

from apps.bookings.serializers import (
    BookingDetailSerializer,
    BookingListSerializer
)


class BookingUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'phone',
            'full_name',
        ]
    def get_full_name(self, obj):
        return obj.get_full_name()


class BookingOwnerListSerializer(BookingListSerializer):
    user = BookingUserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = [
            'user',
            *BookingListSerializer.Meta.fields
        ]



class BookingOwnerDetailSerializer(BookingDetailSerializer):
    user = BookingUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            *BookingDetailSerializer.Meta.fields,
            'user',
        ]




