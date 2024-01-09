from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    message = 'Admin or read only.'

    # Used for listing only (Usually actions are not taken in consideration)
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request=request, view=view)
        if request.method == 'GET' or admin_permission:
            return True
        return False


class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj.review_user == request.user:
                return True
            else:
                return False
