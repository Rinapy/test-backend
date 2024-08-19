from django.db.models import Count
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        pass
        # TODO


@receiver(pre_save, sender=Subscription)
def validate_subscription(sender, instance: Subscription, **kwargs):
    """Сигнал проверки подписки на курс для автора курса."""

    if instance.user == instance.group.course.author:
        raise ValidationError("Нельзя подписаться на свой курс.")
