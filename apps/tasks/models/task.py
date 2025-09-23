from django.core.validators import MinValueValidator
from django.db import models

from apps.tasks.validators import validate_date


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

    def __str__(self):
        return self.topic
