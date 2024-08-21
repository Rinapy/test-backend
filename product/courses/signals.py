from django.db.models import Count
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """
    if created:
        course = instance.course
        groups = course.group_course.annotate(num_subscribers=Count('subscribers')).order_by('num_subscribers')

        if groups.count() < 10:
            # Если групп меньше 10, создаем новую группу
            new_group = Group.objects.create(course=course)
            new_group.subscribers.add(instance.user)
        else:
            # Если групп 10, добавляем в группу с наименьшим количеством участников
            smallest_group = groups.first()
            smallest_group.subscribers.add(instance)
        


@receiver(pre_save, sender=Subscription)
def validate_subscription(sender, instance: Subscription, **kwargs):
    """Сигнал проверки подписки на курс для автора курса."""

    if instance.user == instance.course.author:
        raise ValidationError("Нельзя подписаться на свой курс.")
