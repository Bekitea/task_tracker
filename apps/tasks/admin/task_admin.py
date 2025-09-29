from django.contrib import admin

from apps.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('topic', 'difficulty', 'estimated_hours', 'start_date')
    list_filter = ('difficulty', 'start_date')
    filter_horizontal = ('related_tasks',)
