from .models import TaskModel

import factory


class ParentSingleTaskFactory(factory.Factory):
    class Meta:
        model = TaskModel

    title = factory.Faker('text', length=50)
    description = factory.Faker('text')


# class ParentWithSubsTaskFactory(factory.Factory):
#     class Meta:
#         model = TaskModel

#     title = factory.Faker('text', length=50)
#     description = factory.Faker('text')
#     sub_tasks = factory.Iterator()
