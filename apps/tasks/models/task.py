from django.core.validators import MinValueValidator
from django.db import models

from apps.tasks.validators import validate_date
from task_tracker import settings


class Task(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    DIFFICULTY_CHOICES = [
        (EASY, 'Простая'),
        (MEDIUM, 'Средняя'),
        (HARD, 'Тяжелая'),
    ]

    topic = models.CharField(max_length=63, verbose_name='Тема')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES, verbose_name='Сложность')
    description = models.TextField(blank=True, verbose_name='Описание')
    estimated_hours = models.FloatField(validators=[MinValueValidator(0.01)], verbose_name='Расчетное время')
    start_date = models.DateTimeField(validators=[validate_date], verbose_name='Дата запуска')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Исполнитель'
    )
    related_tasks = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
        verbose_name='Связанные задачи'
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    def __str__(self):
        return f"{self.topic}"

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
