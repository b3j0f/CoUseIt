"""Serialization module."""

from .models import Account, Group, Message, MessageElement
from django.contrib.auth.models import User

from rest_framework.serializers import HyperlinkedModelSerializer


class AccountSerializer(HyperlinkedModelSerializer):
    """Account serializer."""

    class Meta:
        """Account serializer meta class."""

        model = Account
        fields = ['user', 'avatar', 'relationships']


class UserSerializer(HyperlinkedModelSerializer):
    """User serializer."""

    class Meta:
        """User serializer meta class."""

        model = User
        fields = ['account']


class GroupSerializer(AccountSerializer):
    """Group serializer."""

    class Meta:
        """Group serializer meta class."""

        model = Group
        fields = [
            'user', 'avatar', 'relationships', 'name', 'description',
            'account', 'members'
        ]


class MessageSerializer(HyperlinkedModelSerializer):
    """Message serializer."""

    class Meta:
        """Message serializer meta class."""

        model = Message
        fields = ['account']


class MessageElementSerializer(HyperlinkedModelSerializer):
    """MessageElement serializer."""

    class Meta:
        """MessageElement serializer meta class."""

        model = MessageElement
        fields = ['account']
