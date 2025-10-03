from rest_framework import serializers
from apps.tasks.models import Task

from .simple_task_serializer import SimpleTaskSerializer


class TaskWithRelatedSerializer(SimpleTaskSerializer):
    related_tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all(),
        required=False
    )
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

    def process_related_tasks(self, representation, instance):
        representation['related_tasks_info'] = self.get_related_tasks_info(instance)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        self.process_related_tasks(representation, instance)
        return representation