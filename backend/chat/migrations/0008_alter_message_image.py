# Generated by Django 5.1.1 on 2024-10-12 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0007_alter_message_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="room_photo_path/"
            ),
        ),
    ]