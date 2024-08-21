from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Balance


@receiver(post_save, sender=CustomUser)
def create_balance(sender, instance: CustomUser, created, **kwargs):
    """Сигнал создания баланса для нового пользователя."""

    if created:
        instance.balance = Balance.objects.create()
        instance.save()

