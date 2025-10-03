from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied, ValidationError

from apps.core.permissions import IsTaskOwner
from apps.tasks.filters import UserTaskFilter
from apps.tasks.models import Task
from apps.tasks.serializers import TaskWithRelatedSerializer, SimpleTaskSerializer
from apps.tasks.services import create_task, update_task, delete_task, add_related_task, remove_related_task


class UserTaskViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsTaskOwner]
    queryset = Task.objects.select_related('assigned_to').prefetch_related('related_tasks')
    serializer_class = TaskWithRelatedSerializer
    filterset_class = UserTaskFilter

    def get_queryset(self):
        tasks = Task.objects.filter(assigned_to=self.request.user)
        if self.action == 'list':
            return tasks
        return super().get_queryset().filter(assigned_to=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleTaskSerializer
        return super().get_serializer_class()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                task = create_task(serializer.validated_data, request.user)
                response_serializer = self.get_serializer(task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = self.get_serializer(task)
                return Response(response_serializer.data)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = self.get_object()
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = self.get_serializer(updated_task)
                return Response(response_serializer.data)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            delete_task(pk, request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (PermissionDenied, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def add_related_task(self, request, pk=None):
        related_task_id = request.data.get('related_task_id')
        if not related_task_id:
            return Response(
                {'error': 'related_task_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = add_related_task(pk, related_task_id, request.user)
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except (PermissionDenied, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def remove_related_task(self, request, pk=None):
        related_task_id = request.data.get('related_task_id')
        if not related_task_id:
            return Response(
                {'error': 'related_task_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = remove_related_task(pk, related_task_id, request.user)
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except (PermissionDenied, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )