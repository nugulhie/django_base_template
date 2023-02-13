from rest_framework.exceptions import APIException
from rest_framework import status
from django_base_template.libs.utils.STATIC_LITERAL_VALUE import BASE_ERROR
"""
여기서 Custom Exception을 작성하여 코드에 예외처리를 진행합니다.
Exception에 있는 tag와 code를 기입해서 BASE_ERROR에서 에러를 불러옵니다
tag는 BaseModelView에서 선언을 하면 자동으로 기입됩니다.
"""
class BaseCustomException(APIException):
    tag : str
    code : str
    def __init__(self, code: str, tag: str) -> None:
        self.tag = tag
        self.code = code
        super().__init__(self)

class NoneQuerySetReturnError(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "0001"

    def __init__(self, tag: str) -> None:
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag=tag)

    def __str__(self) -> str:
        return self.default_detail

class PermissionDenied(BaseCustomException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "1009"

    def __init__(self, tag: str) -> None:
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag=tag)
    def __str__(self) -> str:
        return self.default_detail

class HTTP404(BaseCustomException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "1008"

    def __init__(self, tag: str) -> None:
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag=tag)

    def __str__(self) -> str:
        return self.default_detail

class AuthenticationFailed(BaseCustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "1007"

    def __init__(self, tag: str) -> None:
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag=tag)

    def __str__(self) -> str:
        return self.default_detail
class NotAuthenticated(BaseCustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "1006"

    def __init__(self, tag: str) -> None:
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag = tag)

    def __str__(self) -> str:
        return self.default_detail


class MethodNotAllowed(BaseCustomException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    code = "0006"

    def __init__(self, tag):
        self.default_detail = BASE_ERROR[self.tag][self.code]
        super().__init__(tag=tag)