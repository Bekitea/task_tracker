from rest_framework import serializers

from apps.tasks.models import Task
from apps.tasks.serializers import SimpleTaskSerializer


class TaskWithUserSerializer(SimpleTaskSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=Task._meta.get_field('assigned_to').remote_field.model.objects.all(),
        allow_null=True,
        required=False
    )
    assigned_to_username = serializers.CharField(read_only=True)

    def process_assigned_user(self, representation, instance):
        representation['assigned_to_username'] = instance.assigned_to.username

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        self.process_assigned_user(representation, instance)
        return representation