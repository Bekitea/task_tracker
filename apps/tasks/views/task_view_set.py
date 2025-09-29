from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied, ValidationError

from apps.tasks.models import Task
from apps.tasks.serializers import TaskWithRelatedSerializer, SimpleTaskSerializer
from apps.tasks.services import get_tasks_for_user, create_task, update_task, delete_task, add_related_task, \
    remove_related_task, get_task


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = get_tasks_for_user(request.user)
        serializer = SimpleTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskWithRelatedSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task = create_task(serializer.validated_data, request.user)
                response_serializer = TaskWithRelatedSerializer(task)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = get_task(request.user, pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskWithRelatedSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = TaskWithRelatedSerializer(data=request.data)
        if serializer.is_valid():
            try:
                task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = TaskWithRelatedSerializer(task)
                return Response(response_serializer.data)
            except (PermissionDenied, ValidationError) as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            task = get_task(request.user, pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskWithRelatedSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_task = update_task(pk, serializer.validated_data, request.user)
                response_serializer = TaskWithRelatedSerializer(updated_task)
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
            serializer = TaskWithRelatedSerializer(task)
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
            serializer = TaskWithRelatedSerializer(task)
            return Response(serializer.data)
        except (PermissionDenied, ValidationError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )