from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from core.enums import Limits

User = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор',
    )

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )

    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    # subscribers = models.ManyToManyField(
    #     User,
    #     related_name='courses_subscribers',
    #     blank=True,
    #     verbose_name='Подписчики курса',
    # )

    price = models.PositiveIntegerField(
        verbose_name='Цена курса',
        validators=[
            MinValueValidator(
                Limits.MIN_COURSE_PRICE,
                message='Минимальная цена курса 0!'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCAD,
        related_name='Группа курса'
    )

    subscribers = models.ManyToManyField(
        User,
        related_name='group_course_subscribers',
        blank=True,
        verbose_name='Состав группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self) -> str:
        return f'Группа курса'