from rest_framework import serializers

from tasks.models import TaskModel


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    model = TaskModel
