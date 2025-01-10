# Generated by Django 5.1.1 on 2024-12-08 13:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0022_room_photo_room"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="message",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="message",
            name="read_by",
            field=models.ManyToManyField(
                blank=True, related_name="read_messages", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]