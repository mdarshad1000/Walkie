from django.forms import ModelForm
from .models import Room


# Creating form based on the db models
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'