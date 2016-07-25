from django.conf.urls import url, include

from rest_framework import routers

from tasks.views import TaskSet

router = routers.DefaultRouter()

router.register(r'tasks', TaskSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
