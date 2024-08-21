from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.core.exceptions import ValidationError


from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAuthorOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer,
                                                  AvailableCourseSerializer)
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.group_course.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAuthorOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )

    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        course = self.get_object()
        user = request.user

        buy_available, buy_already = course.is_available_for(user)

        if buy_already:
            return Response(
                {"detail": "Вы не можете подписатья на курс, на который подписались ранее."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not buy_available:
            return Response(
                {"detail": 'Для подписки на курс не хватает средств.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user.balance.amount -= course.price
            user.balance.save()

            try:
                subscription, created = Subscription.objects.get_or_create(
                    user=user,
                    course=course
                )
            except ValidationError as error:
                return Response(
                    {"detail": error.message},
                    status=status.HTTP_201_CREATED
        )

            if created:
                course.subscribers.add(subscription)

        return Response(
            {"detail": "Вы успешно приобрели курс."},
            status=status.HTTP_201_CREATED
        )

class AvailableBuyCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Доступные для покупки Курсы"""

    serializer_class = AvailableCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.all()

        available_courses = [
            course for course in courses 
            if not course.is_available_for(user)[1] and user != course.author
        ]
        return available_courses

class AvailableLerningCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Доступные для пользователя Курсы"""

    serializer_class = AvailableCourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.all()
        
        available_courses = [
            course for course in courses 
            if course.is_available_for(user)[1]
        ]
        return available_courses