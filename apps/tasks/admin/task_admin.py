from django.contrib import admin, messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils import timezone
from django import forms

from apps.tasks.models import Task
from apps.tasks.services import delete_task, update_task, create_task


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

    def delete_model(self, request, obj):
        try:
            delete_task(obj.id, request.user)
        except (PermissionDenied, ValidationError) as e:
            messages.error(request, f"Ошибка удаления: {str(e)}")
            raise forms.ValidationError(str(e))

    def save_model(self, request, obj, form, change):

        if change:
            try:
                task_data = {
                    'topic': obj.topic,
                    'difficulty': obj.difficulty,
                    'description': obj.description,
                    'estimated_hours': obj.estimated_hours,
                    'start_date': obj.start_date,
                    'assigned_to': obj.assigned_to,
                }

                update_task(obj.id, task_data, request.user)

                if 'related_tasks' in form.cleaned_data:
                    obj.related_tasks.set(form.cleaned_data['related_tasks'])

            except (PermissionDenied, ValidationError) as e:
                messages.error(request, f"Ошибка сохранения: {str(e)}")
                raise forms.ValidationError(str(e))
        else:
            try:
                task_data = {
                    'topic': obj.topic,
                    'difficulty': obj.difficulty,
                    'description': obj.description,
                    'estimated_hours': obj.estimated_hours,
                    'start_date': obj.start_date,
                    'assigned_to': obj.assigned_to,
                    'related_tasks': form.cleaned_data.get('related_tasks', [])
                }

                task = create_task(task_data, request.user)

                obj.id = task.id
                obj.updated_at = task.updated_at

            except (PermissionDenied, ValidationError) as e:
                messages.error(request, f"Ошибка создания: {str(e)}")
                raise forms.ValidationError(str(e))
