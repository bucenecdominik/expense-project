from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class StandingOrderForm(ModelForm):
    class Meta:
        model = StandingOrder
        fields = ['name', 'price', 'description', 'type']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'budget']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ItemForm(ModelForm):
    class Meta: 
        model = Item
        fields = ['price', 'name', 'time_it_was_bought', 'description' ]
