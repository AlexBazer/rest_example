from rest_framework import viewsets, permissions
from tasks.serializers import TaskSerializer
from tasks.models import TaskModel


class TaskViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()
