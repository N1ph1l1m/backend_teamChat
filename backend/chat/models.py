from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from users.models import User

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique = True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "rooms")
    current_users = models.ManyToManyField(User,related_name="current_rooms", blank = True)

    def __str__(self):
        return f"Room({self.name}{self.host})"


def room_photo_path(instance, filename):
    return f'media/photos_rooms/{filename}'


class Photo(models.Model):
    image = models.ImageField(upload_to=room_photo_path)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo({self.id})"

class Message(models.Model):
    room = models.ForeignKey("chat.Room", on_delete= models.CASCADE, related_name="message")
    text = models.TextField(max_length=5000,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,  related_name="messages")
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to=room_photo_path, blank=True)

    def __str__(self):
        return f"Message({self.user}{self.room})"


