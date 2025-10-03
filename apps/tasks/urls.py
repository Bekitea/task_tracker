from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tasks.views import UserTaskViewSet

router = DefaultRouter()
router.register(r'user-tasks', UserTaskViewSet, basename='user-task')
router.register(r'admin-tasks', UserTaskViewSet, basename='admin-task')

app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
]