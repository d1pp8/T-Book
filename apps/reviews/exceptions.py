from apps.common.exceptions import ApplicationError

class BookingNotCompleted(ApplicationError):
    status_code = 409
    default_code = 'booking_not_completed'
    default_detail = 'You can create review for completed bookings.'


class ReviewAlreadyExist(ApplicationError):
    status_code = 409
    default_code = 'review_exists'
    default_detail = 'Review already exists.'


class ReviewOwnershipError(ApplicationError):
    status_code = 403
    default_code = 'review_ownership_error'
    default_detail = 'Review belongs to someone else.'