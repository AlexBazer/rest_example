from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions

from users.serializers import UserSerializer

User = get_user_model()


class UserViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
