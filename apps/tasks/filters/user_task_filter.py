import django_filters
from apps.tasks.models import Task


class UserTaskFilter(django_filters.FilterSet):
    difficulty = django_filters.ChoiceFilter(
        choices=Task.DIFFICULTY_CHOICES,
        label='Сложность'
    )

    class Meta:
        model = Task
        fields = ['difficulty']