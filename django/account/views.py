"""View module."""

from django.contrib.auth.models import User
from .models import Account, Group, Message, MessageElement
from .serializers import (
    AccountSerializer, UserSerializer, GroupSerializer, MessageSerializer,
    MessageElementSerializer
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


class GroupViewSet(AccountViewSet):
    """Group view set."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = {
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'members': ['exact']
    }


class MessageViewSet(ModelViewSet):
    """Message view set."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_fields = {
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'members': ['exact']
    }


class MessageElementViewSet(ModelViewSet):
    """MessageElement view set."""

    queryset = MessageElement.objects.all()
    serializer_class = MessageElementSerializer
    filter_fields = {
        'name': ['exact', 'icontains'],
        'description': ['icontains'],
        'members': ['exact']
    }
