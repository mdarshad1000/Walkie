from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
# from django.contrib.auth.models import User
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


# Creating form based on the db models
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        