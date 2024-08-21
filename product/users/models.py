from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint, Q
from core.enums import Limits


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=250
    )

    balance = models.OneToOneField(
        'Balance',
        on_delete=models.SET_NULL,
        verbose_name='Баланс пользователя',
        related_name='user',
        null=True,
        blank=True,
    )

    is_creator = models.BooleanField(
        verbose_name='Пользователь может создавать курсы.',
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    amount = models.PositiveIntegerField(
        verbose_name='Доступный баланс',
        default=Limits.START_BALANCE,
        validators=[
            MinValueValidator(
                Limits.MIN_BALANCE_AMOUNT,
                message='Минимальный баланс пользователя 0!'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        related_name='subscriptions',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='subscriptions',
        verbose_name="Курс",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'course'],
                name='unique_subscription'),
        ]
