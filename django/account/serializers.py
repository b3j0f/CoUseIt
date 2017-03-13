"""Serialization module."""

from .models import Account
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
        fields = ['account', ]