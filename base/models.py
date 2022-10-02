from hashlib import blake2b
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # Many to many relationship
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # Takes a snapshot everytime we save
    updated = models.DateTimeField(auto_now=True)
    # Takes a snapshot only when created
    created = models.DateTimeField(auto_now_add=True)

    # To view the newest Room first
    class Meta:
        ordering = ['-updated', '-created']




    # string representation 
    def __str__(self):
        return self.name



class Message(models.Model):
    # One to Many relatoinship, hence the foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # To view the newest Message first
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        # Display first 50 characters 
        return self.body[0:50]






'''
on_delete=models.CASCADE --> In case of Room Model, if Topic gets deleted then the room gets deleted too.
on_delete=models.SET_NULL --> In case of Room Model, if Topic gets deleted then the room doesn't get deleted.
                              Only the value of Topic is set to Null.
'''