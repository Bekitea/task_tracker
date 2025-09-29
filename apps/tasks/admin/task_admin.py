from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.tasks.models import Task
from apps.tasks.validators import validate_date


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('topic', 'difficulty', 'estimated_hours', 'start_date', 'assigned_to', 'can_edit')
    list_filter = ('difficulty', 'start_date', 'assigned_to')
    filter_horizontal = ('related_tasks',)
    readonly_fields = ('updated_at',)

    def can_edit(self, obj):
        return obj.start_date > timezone.now()

    can_edit.boolean = True
    can_edit.short_description = 'Можно редактировать'

    def save_model(self, request, obj, form, change):
        if change and obj.start_date <= timezone.now():
            raise ValidationError("Нельзя редактировать задачу, у которой дата запуска уже наступила")

        super().save_model(request, obj, form, change)