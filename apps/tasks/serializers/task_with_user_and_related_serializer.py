from .task_with_related_serializer import TaskWithRelatedSerializer
from .task_with_user_serializer import TaskWithUserSerializer


class TaskWithUserAndRelatedSerializer(TaskWithUserSerializer, TaskWithRelatedSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        self.process_related_tasks(representation, instance)
        return representation