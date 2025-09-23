from datetime import datetime
from django.utils import timezone

from apps.tasks.errors import InvalidDateError


def validate_date(value: datetime):
    if value <= timezone.now():
        raise InvalidDateError(value)
