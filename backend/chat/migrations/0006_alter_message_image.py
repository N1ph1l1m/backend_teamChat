# Generated by Django 5.1.1 on 2024-10-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_message_photos_message_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, upload_to='room_photo_path/'),
        ),
    ]
