# Generated by Django 5.1.1 on 2024-10-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0008_alter_message_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="image",
            field=models.ImageField(blank=True, upload_to="room_photo_path/"),
        ),
        migrations.AlterField(
            model_name="message",
            name="text",
            field=models.TextField(blank=True, default=1, max_length=5000),
            preserve_default=False,
        ),
    ]
