from .models import TaskModel

import factory


class TaskFactory(factory.Factory):
    class Meta:
        model = TaskModel

    title = factory.Faker('text', max_nb_chars=10)
    description = factory.Faker('text')
