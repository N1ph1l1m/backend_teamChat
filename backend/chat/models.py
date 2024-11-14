from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from users.models import User
import os

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique = True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "rooms")
    current_users = models.ManyToManyField(User,related_name="current_rooms", blank = True)

    def __str__(self):
        return f"Room({self.name}{self.host})"


def room_photo_path(instance, filename):
    return f'media/photos_rooms/{filename}'


class Photos(models.Model):
    image = models.ImageField(upload_to='room_photo_path/', blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo({self.id})"


class Documents(models.Model):
    document = models.FileField(upload_to='room_file_path/', blank=True)
    name = models.CharField(max_length=255, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Если поле name пустое, устанавливаем только имя файла без пути
        if self.document and not self.name:
            self.name = os.path.basename(self.document.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Document({self.id})"

class Message(models.Model):
    room = models.ForeignKey("chat.Room", on_delete= models.CASCADE, related_name="message")
    text = models.TextField(max_length=5000,blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,  related_name="messages")
    created_at = models.DateTimeField(auto_now_add = True)
    images = models.ManyToManyField(Photos, related_name="photos")
    documents = models.ManyToManyField(Documents,related_name="documents")
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="replies")

    def __str__(self):
        return f"Message({self.user}{self.room})"


