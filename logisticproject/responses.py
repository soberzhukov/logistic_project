from rest_framework.response import Response
from typing import Optional, TypeVar


AnyDict = TypeVar('AnyDict', dict, None)


class BaseResponse(Response):
    status_code: int = None

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None, data: Optional[dict] = None):
        if data is not None:
            self.data = data
        else:
            self.data = self._generate_data(message, code)
        super().__init__(self.data, self.status_code)

    @staticmethod
    def _generate_data(message: Optional[str] = None, code: Optional[str] = None) -> AnyDict:
        if message and code:
            return {'message': message, 'code': code}
        else:
            return None


class AccessResponse(BaseResponse):
    status_code = 200

    def __init__(self, message: Optional[str] = None, code: Optional[str] = None, data: Optional[dict] = None):
        if data is None:
            if not (message and code):
                data = {'message': 'ok'}
        super().__init__(message, code, data)


class BadeRequestResponse(BaseResponse):
    status_code = 400


class ForbiddenResponse(BaseResponse):
    status_code = 404


class CreatedResponse(BaseResponse):
    status_code = 201


class NotContentResponse(BaseResponse):
    status_code = 204