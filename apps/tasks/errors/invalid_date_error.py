from datetime import datetime

from django.core.exceptions import ValidationError


class InvalidDateError(ValidationError):
    def __init__(self, value: datetime):
        self.value = value

    def __str__(self):
        return f'Время запуска задачи должно быть в будущем, {self.value} не подходит.'
