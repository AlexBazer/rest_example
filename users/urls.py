from django.conf.urls import url, include

from rest_framework import routers

from users.views import UserViewset

router = routers.DefaultRouter()
router.register('users', UserViewset)

urlpatterns = [
    url(r'^', include(router.urls))
]
