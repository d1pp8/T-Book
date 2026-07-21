from rest_framework.exceptions import APIException
from rest_framework import status


class PropertyHasActiveBookings(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'property_has_active_bookings'
    default_detail = 'The property cannot be deleted because it has active bookings.'


class UnitHasActiveBookings(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'Unit_has_active_bookings'
    default_detail = 'The unit cannot be deleted because it has active bookings.'