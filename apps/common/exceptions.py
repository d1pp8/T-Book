from rest_framework.exceptions import APIException

class ApplicationError(APIException):
    status_code = 400
    default_code = "application_error"
    default_detail = "Application error."