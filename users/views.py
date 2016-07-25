from rest_framework import viewsets
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer

User = get_user_model()


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
