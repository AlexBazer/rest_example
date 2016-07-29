from rest_framework import serializers

from tasks.models import TaskModel


class SubTaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TaskModel
        fields = ('url', 'id', 'title', 'description')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    sub_tasks = SubTaskSerializer(many=True, required=False)

    def create(self, validated_data):
        """Create subtask if exists"""
        sub_tasks = validated_data.pop('sub_tasks')
        task = self.Meta.model.objects.create(**validated_data)
        for sub in sub_tasks:
            self.Meta.model.objects.create(parent=task, **sub)

        return task

    def update(self, instance, validated_data):
        """Update task data.

        Handles nested sub_tasks

        If empty sub_tasks in request - remove all subtasks
        If no sub_tasks in request - do leave them alone
        If sab_task without id, create new one
        If sub_task id not in sub_tasks, create new one
        Also removes tasks that was not in request
        """
        sub_tasks = validated_data.pop('sub_tasks', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if sub_tasks is None:
            return instance

        existing_sub_tasks = instance.sub_tasks.all()
        existing_sub_task_ids = existing_sub_tasks.values_list('id', flat=True)
        updated_ids = [item['id'] for item in sub_tasks if 'id' in item]
        subs_to_delete = set(existing_sub_task_ids) - set(updated_ids)
        if subs_to_delete:
            TaskModel.objects.filter(id__in=list(subs_to_delete)).delete()

        def update_or_create_task(task_data):
            """Update sub task data if it was send with id, otherwise create new one """

            task = None
            if 'id' in task_data:
                try:
                    task = TaskModel.objects.get(id=task_data['id'])
                except TaskModel.DoesNotExist:
                    task_data.pop('id')
                    pass
            if not task:
                task = TaskModel.objects.create()

            for key, value in task_data.items():
                setattr(task, key, value)
            task.parent = instance

            task.save()

        [update_or_create_task(item) for item in sub_tasks]

        return instance

    class Meta:
        model = TaskModel
        fields = ('url', 'id', 'title', 'description', 'sub_tasks', 'parent')
