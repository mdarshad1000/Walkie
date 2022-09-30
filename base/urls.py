from django.urls import path
from . import views

urlpatterns = [
    # good practice to name it too and is convinient for accessing in templates.
    path('', views.home, name='home'), 
    path('room/<str:pk>', views.room, name='room')
]