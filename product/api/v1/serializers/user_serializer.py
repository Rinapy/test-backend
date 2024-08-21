from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            '__all__'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    course_name = serializers.SerializerMethodField()
    subs = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'course_name',
            'subs',
        )

    def get_course_name(self, obj):
        return obj.course.title

    def get_subs(self, obj):
        return list(obj.course.subscribing.values_list('user', flat=True))

