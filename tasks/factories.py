from .models import TaskModel

import factory


class TaskFactory(factory.Factory):
    class Meta:
        model = TaskModel
    title = factory.Faker('text', length=10)
    description = factory.Faker('text')
