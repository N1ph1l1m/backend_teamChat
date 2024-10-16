# Generated by Django 5.1.1 on 2024-10-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_alter_message_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='room_photo_path/')),
                ('upload_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.RemoveField(
            model_name='message',
            name='image',
        ),
        migrations.AddField(
            model_name='message',
            name='images',
            field=models.ManyToManyField(related_name='photos', to='chat.photos'),
        ),
    ]
