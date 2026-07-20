from apps.common.exceptions import ApplicationError



class UnitNotAvailable(ApplicationError):
    status_code = 409
    default_code = 'unit_not_available'
    default_detail = 'Unit is not available.'


class InvalidBookingDate(ApplicationError):
    status_code = 400
    default_code = 'invalid_dates'
    default_detail = 'Invalid dates.'


class CapacityExceeded(ApplicationError):
    status_code = 409
    default_code = 'number_of_people_error'
    default_detail = 'Number of people error.'


class BookingStateConflict(ApplicationError):
    status_code = 409
    default_code = 'invalid_booking_status'
    default_detail = 'Booking status transition is not allowed.'


class InvalidCancellation(ApplicationError):
    status_code = 409
    default_code = 'invalid_cancellation'
    default_detail = 'The cancellation period for this booking has expired.'