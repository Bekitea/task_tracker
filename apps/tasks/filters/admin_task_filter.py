import django_filters
from django.contrib.auth import get_user_model
from apps.tasks.models import Task

class AdminTaskFilter(django_filters.FilterSet):
    assigned_to = django_filters.ModelChoiceFilter(
        queryset=get_user_model().objects.all(),
        label='Assigned User'
    )
    difficulty = django_filters.ChoiceFilter(
        choices=Task.DIFFICULTY_CHOICES,
        label='Сложность'
    )

    class Meta:
        model = Task
        fields = [
            'assigned_to', 
            'difficulty'
        ]