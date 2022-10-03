from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Room


# Creating form based on the db models
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        