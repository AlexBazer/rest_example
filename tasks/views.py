from rest_framework import viewsets

from tasks.serializers import TaskSerializer


class TaskSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
