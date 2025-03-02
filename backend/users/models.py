from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография", default="users/default_avatar.jpg")
    data_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    last_active = models.DateTimeField(blank=True, null=True, verbose_name="Последняя активность")