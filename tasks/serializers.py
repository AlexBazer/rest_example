from rest_framework import serializers

from tasks.models import TaskModel


class SubTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskModel
        fields = ('url', 'title', 'description')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    sub_tasks = SubTaskSerializer(many=True)

    class Meta:
        model = TaskModel
        fields = ('url', 'title', 'description', 'sub_tasks', 'parent')
