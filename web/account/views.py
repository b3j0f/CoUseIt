"""View module."""

from django.contrib.auth.models import User
from .models import Account
from .serializers import (
    AccountSerializer, UserSerializer
)

from rest_framework.viewsets import ModelViewSet


class AccountViewSet(ModelViewSet):
    """Account view set."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_fields = {
        'id': ['exact'],
        'user': ['exact'],
        'relationships': ['exact', 'in']
    }


class UserViewSet(ModelViewSet):
    """User view set."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = {
        'id': ['exact'],
        'username': ['exact'],
        'email': ['exact']
    }
