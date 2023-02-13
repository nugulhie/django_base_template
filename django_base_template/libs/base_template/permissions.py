from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
    """
    조건문을 통해서
    return True, return False 값으로 권한을 확인합니다.
    """
    pass

class UserPermission(CustomPermission):
    def has_permission(self, request, view):
        """
        여기서 권한 확인 로직을 넣는다.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        여기서 권한 확인 로직을 넣는다.
        """
        return True

