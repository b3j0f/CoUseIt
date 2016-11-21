"""Forms module."""

from .models import Stock, Status

from django import forms
from address.forms import AddressField


class StockForm(forms.Form):
    address = AddressField()


class PlanningForm(forms.Form):

    status = forms.TypedChoiceField(choices=Status.choices, coerce=int)
