from datetime import datetime
from django.utils import timezone

from django.forms import ValidationError


def validate_date(value: datetime):
    if value <= timezone.now():
        raise ValidationError(f'Время запуска задачи должно быть в будущем, {value} не подходит.')
