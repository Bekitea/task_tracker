from django.utils import timezone
from rest_framework import serializers

from apps.tasks.models import Task
from apps.tasks.validators import validate_date


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'topic', 'difficulty', 'description',
            'estimated_hours', 'start_date',
            'assigned_to', 'updated_at',
            'assigned_to_username'
        ]
        read_only_fields = ['updated_at']
