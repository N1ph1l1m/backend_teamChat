from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from users.models import User
import os
from django.db import transaction

class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique = True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "rooms")
    current_users = models.ManyToManyField(User,related_name="current_rooms", blank = True)
    photo_room = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография", default="users/default_groupChat.png")

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



class ReactionToMessage(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10,blank=True,null=True)
    def __str__(self):
        return f"Reaction({self.id_user}, {self.emoji})"


class ForwardedMessage(models.Model):
    original_message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, related_name="forwarded_messages_from", blank=True
    )
    forwarded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="forwarded_by_user"
    )
    forwarded_to_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="forwarded_to_room"
    )
    forwarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ForwardedMessage(from {self.original_message.id} to {self.forwarded_to_room.name})"


class Message(models.Model):
    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="message")
    text = models.TextField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    reactions = models.ManyToManyField(ReactionToMessage, related_name="reactions_to_message" , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Photos, related_name="photos", blank=True)
    documents = models.ManyToManyField(Documents, related_name="documents", blank=True)
    reply_to = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies'
    )
    forwarded_messages = models.ManyToManyField(ForwardedMessage,  related_name='forwarded_to_messages', blank=True)
    is_read =  models.BooleanField(default=False)
    read_by = models.ManyToManyField(User,related_name="read_messages",blank=True)
    read_at = models.DateTimeField(null=True,blank=True)

    @staticmethod
    @transaction.atomic
    def forward_multiple_messages(user, room, messages):
        forwarded_messages = []

        for message in messages:
            forwarded_message = Message.objects.create(
                text=message.text,
                user=user,
                room=room,
                reply_to=message.reply_to,
            )
            # Переносим связанные объекты, если нужно
            forwarded_message.images.set(message.images.all())
            forwarded_message.documents.set(message.documents.all())
            forwarded_messages.append(forwarded_message)

        return forwarded_messages

    def __str__(self):
        user = self.user.username if self.user else "Unknown User"
        room = self.room.name if self.room else "Unknown Room"
        return f"Message from {user} in room {room}"
