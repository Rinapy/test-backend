from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from api.v1.serializers.user_serializer import CustomUserSerializer, SubscriptionSerializer, Subscription

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Подписки."""
    
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)