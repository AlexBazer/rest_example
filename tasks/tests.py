from rest_framework import test, status
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from .models import TaskModel
from .factories import TaskFactory
from factory import fuzzy

User = get_user_model()


class TaskCreateUpdateTestCase(test.APITestCase):
    def setUp(self):
        self.user_password = 'sometestPa33'
        self.user = User(username='test')
        self.user.set_password(self.user_password)
        self.user.save()
        self.client.login(
            username=self.user.username,
            password=self.user_password
        )
        self.parent_task = TaskFactory()
        self.parent_task.save()
        self.children_tasks = TaskFactory.create_batch(3, parent=self.parent_task)
        [item.save() for item in self.children_tasks]

    def test_task_create_with_nested(self):
        """ Create new note with nested tasks as children """
        parent_title = "Prent task for test_task_create_with_nested"
        response = self.client.post(reverse('taskmodel-list'), {
            'title': parent_title,
            'description': 'Test description',
            'sub_tasks': [
                {
                    'title': 'Test 1',
                    'description': 'Test description'
                },
                {
                    'title': 'Test 2',
                    'description': 'Test description'
                }
            ]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_parent = TaskModel.objects.get(title=parent_title)
        created_children = created_parent.sub_tasks.all()
        self.assertEqual(created_children.count(), 2)

    def test_task_update_with_nested(self):
        """ Update parent task fields and childeren task fields

        sub_tasks will include all earlier created children ids with new title each
        """
        new_children_tasks = [
            {
                'id': item.id,
                'title': fuzzy.FuzzyText().fuzz(),
                'description': item.description
            } for item in self.children_tasks
        ]

        new_parent_task = {
            'title': fuzzy.FuzzyText().fuzz(),
            'description': self.parent_task.description
        }
        new_parent_task['sub_tasks'] = new_children_tasks
        response = self.client.put(
            reverse('taskmodel-detail', kwargs={'pk': self.parent_task.id}),
            new_parent_task,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get object from db
        parent_task = TaskModel.objects.get(id=self.parent_task.id)
        children_tasks = TaskModel.objects.filter(
            id__in=[item.id for item in self.children_tasks]
        )
        # Compare db parent task title and new one
        self.assertEqual(parent_task.title, new_parent_task['title'])

        # Compare db subtasks title with new ones
        [
            self.assertEqual(item[1].title, item[0]['title'])
            for item in zip(new_children_tasks, children_tasks)
        ]
