from rest_framework.permissions import BasePermission
from .models import User


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.STUDENT
        )
    
class IsLecturer(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.LECTURER
        )
    
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )
    
class IsLecturerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.LECTURER,
                User.Role.ADMIN
            ]
        )