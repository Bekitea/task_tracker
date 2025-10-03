from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction

from apps.tasks.models import Task
from apps.tasks.validators import validate_date

def can_edit_task(task, user):
    if task.start_date < timezone.now():
        return False

    return True

def create_task(task_data, user):
    validate_date(task_data['start_date'])

    if not user.is_superuser:
        task_data['assigned_to'] = user

    with transaction.atomic():
        related_tasks_data = task_data.pop('related_tasks', [])

        task = Task.objects.create(**task_data)

        if related_tasks_data:
            task.related_tasks.set(related_tasks_data)

        return task

def update_task(task_id, task_data, user):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise ValidationError("Задача не найдена")

    if not can_edit_task(task, user):
        raise PermissionDenied("Вы не можете редактировать эту задачу")

    if 'start_date' in task_data:
        validate_date(task_data['start_date'])

    with transaction.atomic():
        related_tasks_data = task_data.pop('related_tasks', None)

        for field, value in task_data.items():
            setattr(task, field, value)

        task.save()

        if related_tasks_data is not None:
            task.related_tasks.set(related_tasks_data)

        return task

def delete_task(task_id, user):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise ValidationError("Задача не найдена")

    task.delete()

def add_related_task(task_id, related_task_id, user):
    try:
        task = Task.objects.get(id=task_id)
        related_task = Task.objects.get(id=related_task_id)
    except Task.DoesNotExist:
        raise ValidationError("Задача не найдена")

    if not can_edit_task(task, user):
        raise PermissionDenied("Вы не можете редактировать эту задачу")

    task.related_tasks.add(related_task)
    return task

def remove_related_task(task_id, related_task_id, user):
    try:
        task = Task.objects.get(id=task_id)
        related_task = Task.objects.get(id=related_task_id)
    except Task.DoesNotExist:
        raise ValidationError("Задача не найдена")

    if not can_edit_task(task, user):
        raise PermissionDenied("Вы не можете редактировать эту задачу")

    task.related_tasks.remove(related_task)
    return task