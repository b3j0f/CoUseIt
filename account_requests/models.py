from django.db import models

from django.contrib.auth.models import User


class CRUD(models.Model):
    name = models.CharField(max_length=6, primary_key=True)


class StateRequest(models.Model):
    name = models.CharField(max_length=10, primary_key=True)


class AccountRequest(models.Model):
    """Permits to a user to ask to realize specific actions on the model."""

    account = models.ForeignKey(User)
    creation = models.DateTimeField()

    action = models.ForeignKey(CRUD)

    srcmodel = models.CharField(max_length=500)
    targetmodel = models.CharField(max_length=500)

    relationship = models.CharField(max_length=500)

    srcmodelid = models.BigIntegerField()
    targetmodelid = models.BigIntegerField()

    state = models.ForeignKey(StateRequest)

    comment = models.CharField(max_length=1024)
    answer = models.CharField(max_length=1024)
    answer_date = models.DateTimeField()
