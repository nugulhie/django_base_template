from rest_framework.views import set_rollback
from django_base_template.libs.base_template.response import ReturnResponse
from django_base_template.libs.base_template.exceptions import HTTP404, PermissionDenied, BaseCustomException

def exception_handler(exc, context):
    if isinstance(exc, HTTP404):
        exc = HTTP404(tag=exc.tag)
    elif isinstance(exc, PermissionDenied):
        exc = PermissionDenied(tag=exc.tag)

    if isinstance(exc, BaseCustomException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = {"code":exc.code, "message":exc.default_detail}
        else:
            data = {"code":exc.code, "message":exc.default_detail}

        set_rollback()
        return ReturnResponse(flag=False, data=data, status=exc.status_code, headers=headers)
    else:

        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        set_rollback()
        return ReturnResponse(flag=False, data={{"code": "0005", "message": "알수 없는 에러"}}, status=exc.status_code, headers=headers)