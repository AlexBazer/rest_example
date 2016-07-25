from django.db import models


class TaskModel(models.Model):
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description')
    created = models.DateTimeField('Created', auto_now_add=True)
    parent = models.ForeignKey('self', null=True, default=None, related_name='sub_tasks')
