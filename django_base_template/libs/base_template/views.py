from rest_framework import status
from rest_framework import viewsets, permissions
from typing import Protocol

from django_base_template.libs.base_template.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied, MethodNotAllowed
from django_base_template.libs.utils.Logger import Logging

class BaseAdminView(viewsets.ModelViewSet):
    permission_classes : list(permissions.BasePermission)
    operation : Protocol # 이런식으로 추가적인 변수를 선언해줄수 도 있다.
    logger : Logging # Exception이 발생했을 때 Log를 찍어주기 위한 Logger이다
    tag = "BASE" # 나는 Exception에 Tag를 넣어서 서비스에 맞는 Error Message를 띄워주기 위해서 선언한다.
    def __init__(self, operation, permission : permissions.BasePermission):
        self.operation = operation
        self.permission_classes.append(permission)
        super().__init__()

    def check_object_permissions(self, request, obj):
        """
        여기서 Object에 관한 permission을 확인하는데 추가적인 행동을 여기서 제어한다.
        """
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def check_permissions(self, request):
        """
        APIView에 있는 permission_classes에서 받지 못한 추가적인 행동을 여기서 Custom 할 수 있다
        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def http_method_not_allowed(self, request, *args, **kwargs):
        """여기서 method_not_allowed 오류를 반환하는 곳이다. 
        405에러를 띄울 때 필요한 행동을 여기서 정의한다
        """
        raise MethodNotAllowed(self.tag)

    def handle_exception(self, exc):
        """여기서 exception을 통해 Response를 반환한다
        Args:
            exc (_type_): 이 친구는 Exception이다
            Exception을 커스텀 하는 이유도 오류에서 Reponse를 커스텀 하기 위해서다
        """
        
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        view_name = self.get_view_name()
        self.logger.exception(view_name, exc)
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)
        
        response.exception = True
        return response

    def permission_denied(self, request, message=None, code=None):
        """
        여기에 커스텀 Auth를 넣음
        """
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated(tag=self.tag)
        raise PermissionDenied(tag=self.tag)

    def get_exception_handler(self):
        """
        Settings안에 EXCEPTION_HANDLER를 선언한다
        """
        return self.settings.EXCEPTION_HANDLER
