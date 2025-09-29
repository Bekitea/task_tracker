from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

app_name = 'tasks'
urlpatterns = [
    path('', include(router.urls)),
]