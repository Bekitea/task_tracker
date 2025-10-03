from django.core.exceptions import ValidationError
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsAdmin
from apps.tasks.filters import AdminTaskFilter
from apps.tasks.models import Task
from apps.tasks.serializers import TaskWithUserAndRelatedSerializer, TaskWithUserSerializer
from apps.tasks.services import create_task, update_task, delete_task, add_related_task, remove_related_task


class AdminTaskViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Task.objects.select_related('assigned_to').prefetch_related('related_tasks')
    serializer_class = TaskWithUserAndRelatedSerializer
    filterset_class = AdminTaskFilter

    def get_queryset(self):
        tasks = Task.objects.select_related('assigned_to')
        if self.action == 'list':
            return tasks
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskWithUserSerializer
        return super().get_serializer_class()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = create_task(serializer.validated_data, request.user)
            response_serializer = self.get_serializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = update_task(pk, serializer.validated_data, request.user)
            response_serializer = self.get_serializer(task)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            updated_task = update_task(pk, serializer.validated_data, request.user)
            response_serializer = self.get_serializer(updated_task)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        delete_task(pk, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def add_related_task(self, request, pk=None, related_task_id=None):
        if not related_task_id:
            raise ValidationError('related_task_id обязателен')

        task = add_related_task(pk, related_task_id, request.user)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_related_task(self, request, pk=None, related_task_id=None):
        if not related_task_id:
            raise ValidationError('related_task_id обязателен')

        task = remove_related_task(pk, related_task_id, request.user)
        serializer = self.get_serializer(task)
        return Response(serializer.data)
