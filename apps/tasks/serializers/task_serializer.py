from rest_framework import serializers

from apps.tasks.models import Task
from apps.tasks.validators import validate_date


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    #
    # def validate_start_date(self, value):
    #     validate_date(value)
    #     return value
