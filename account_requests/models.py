from django.db import models

from django.contrib.auth.models import User


class CRUD(models.Model):
    name = models.CharField(max_length=6, primary_key=True)

    def __str__(self):

        return 'CRUD: {0}'.format(self.name)


class StateRequest(models.Model):
    name = models.CharField(max_length=11, primary_key=True)

    def __str__(self):

        return 'RequestState: {0}'.format(self.name)


class AccountRequest(models.Model):
    """Permits to a user to ask to realize specific actions on the model."""

    user = models.ForeignKey(User)
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

    def __str__(self):

        return 'Request(user: {0}, creation: {1}, action: {2}, state: {3}, comment: {4})'.format(self.user, self.creation, self.action, self.state, self.comment)