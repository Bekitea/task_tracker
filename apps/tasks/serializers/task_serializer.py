from rest_framework import serializers
from apps.tasks.models import Task
from apps.tasks.validators import validate_date


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=63)
    difficulty = serializers.ChoiceField(choices=Task.DIFFICULTY_CHOICES)
    description = serializers.CharField(allow_blank=True, required=False)
    estimated_hours = serializers.FloatField(min_value=0.01)
    start_date = serializers.DateTimeField(validators=[validate_date])
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Task._meta.get_field('assigned_to').remote_field.model.objects.all(),
        allow_null=True,
        required=False
    )
    related_tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
    updated_at = serializers.DateTimeField(read_only=True)

    assigned_to_username = serializers.CharField(read_only=True)
    related_tasks_info = serializers.SerializerMethodField(read_only=True)

    def get_related_tasks_info(self, obj):
        return [
            {
                'id': task.id,
                'topic': task.topic,
                'difficulty': task.difficulty
            }
            for task in obj.related_tasks.all()
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['related_tasks_info'] = self.get_related_tasks_info(instance)
        representation['assigned_to_username'] = instance.assigned_to.username
        return representation