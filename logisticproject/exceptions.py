from rest_framework import status
from rest_framework.exceptions import APIException


class BaseException(APIException):
    status_code = None

    def __init__(self, message, code):
        self._message = message
        self._code = code
        self.detail = {'code': self._code, 'message': self._message}


class BadeRequestException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST


class ForbiddenException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN


class AccessException(BaseException):
    status_code = status.HTTP_200_OK
