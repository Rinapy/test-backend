from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404

from courses.models import Course


class IsStudentOrIsAdmin(BasePermission):
    """
    Разрешение позволяет доступ, если пользователь является подписчиком курса,
    автором курса или администратором.
    """

    def has_permission(self, request, view):
        
        course_id = view.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        if request.user.is_staff:
            return True

        if course.author == request.user:
            return True

        if course.subscribers.filter(user=request.user).exists():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        course = obj.course

        if request.user.is_staff:
            return True

        if course.author == request.user:
            return True

        if course.subscribers.filter(id=request.user.id).exists():
            return request.method in SAFE_METHODS

        return False
        
class ReadOnlyOrIsCreatorOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS or request.user.is_creator

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS or obj.author == request.user

class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
