from rest_framework import serializers

from apps.tasks.models import Task
from apps.tasks.validators import validate_date


class SimpleTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=63)
    difficulty = serializers.ChoiceField(choices=Task.DIFFICULTY_CHOICES)
    description = serializers.CharField(allow_blank=True, required=False)
    estimated_hours = serializers.FloatField(min_value=0.01)
    start_date = serializers.DateTimeField(validators=[validate_date])
    updated_at = serializers.DateTimeField(read_only=True)