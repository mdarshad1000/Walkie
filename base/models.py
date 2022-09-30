from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Room(models.Model):
    # host = 
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = 
    # Takes a snapshot everytime we save
    updated = models.DateTimeField(auto_now=True)
    # Takes a snapshot only when created
    created = models.DateTimeField(auto_now_add=True)