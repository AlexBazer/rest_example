from rest_framework import viewsets

from tasks.serializers import TaskSerializer
from tasks.models import TaskModel


class TaskSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()
