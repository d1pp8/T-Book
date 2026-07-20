from apps.bookings.choices import BookingStatus

from apps.bookings.models import Booking
from apps.reviews.models import Review
from apps.users.models import User

from apps.reviews.exceptions import (
    ReviewOwnershipError,
    BookingNotCompleted,
    ReviewAlreadyExist
)


class ReviewValidator:
    @staticmethod
    def validate_owner(user: User, booking: Booking) -> None:
        if booking.user != user:
            raise ReviewOwnershipError

    @staticmethod
    def validate_completed(booking: Booking) -> None:
        if booking.status != BookingStatus.COMPLETED:
            raise BookingNotCompleted

    @staticmethod
    def validate_review_exists(booking: Booking) -> None:
        if Review.objects.filter(booking=booking).exists():
            raise ReviewAlreadyExist