from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied, ValidationError

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from apps.tasks.services import get_tasks_for_user, create_task, update_task, delete_task, add_related_task, \
    remove_related_task


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_tasks_for_user(self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task = create_task(serializer.validated_data, request.user)
                response_serializer = TaskSerializer(task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = TaskSerializer(task)
                return Response(response_serializer.data)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = TaskSerializer(updated_task)
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
            serializer = TaskSerializer(task)
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
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except (PermissionDenied, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )