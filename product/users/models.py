from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint, CheckConstraint
from django.db.models import F

from courses.models import Group

from core.enums import Limits


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=250
    )

    balance = models.ForeignKey(
        'Balance',
        on_delete=models.CASCADE,
        verbose_name='Баланс пользователя',
        related_name='balance'
    )

    is_author = models.BooleanField(
        verbose_name='Пользователь являеться преподователем.'
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
        verbose_name='Баланс',
        default=1000,
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
        related_name='subscriber',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    # course = models.ForeignKey(
    #     Course,
    #     related_name='subscribing',
    #     verbose_name="Курс",
    #     on_delete=models.CASCADE,
    # )
    group = models.ManyToManyField(
        Group,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Группа',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'group__course'],
                name='unique_subscription'),
            CheckConstraint(
                check=~(models.Q(user=F('group__course__author'))),
                name='author_cannot_subscribe_to_own_course')
        ]
