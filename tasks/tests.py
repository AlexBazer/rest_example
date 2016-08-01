from rest_framework import test, status
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from .models import TaskModel
from .factories import ParentSingleTaskFactory

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
        """ Update parent task fields """
        pass