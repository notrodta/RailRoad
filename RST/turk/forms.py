from django.contrib.auth.models import User
from django import forms
from .models import *


class PassengerForm(forms.ModelForm):

    class Meta:
        model = Passenger
        fields = ['fname', 'lname', 'billing_address']

class SeatfreeForm(forms.ModelForm):

    class Meta:
        model = Seats_Free
        fields = ['seat_free_date']