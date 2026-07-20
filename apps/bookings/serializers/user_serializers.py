from apps.bookings.serializers import (
    BookingCreateSerializer,
    BookingDetailSerializer,
    BookingListSerializer
)


class BookingUserCreateSerializer(BookingCreateSerializer):
    pass


class BookingUserListSerializer(BookingListSerializer):
    pass


class BookingUserDetailSerializer(BookingDetailSerializer):
    pass

