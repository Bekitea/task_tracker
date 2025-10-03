from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tasks.views import UserTaskViewSet, AdminTaskViewSet

router = DefaultRouter()
router.register(r'user-tasks', UserTaskViewSet, basename='user-task')
router.register(r'admin-tasks', AdminTaskViewSet, basename='admin-task')

app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
]