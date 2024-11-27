# Generated by Django 5.1.1 on 2024-11-27 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_message_forwarded_from'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='forwarded_from',
        ),
        migrations.CreateModel(
            name='ForwardedMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forwarded_at', models.DateTimeField(auto_now_add=True)),
                ('forwarded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarded_by_user', to=settings.AUTH_USER_MODEL)),
                ('forwarded_to_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forwarded_to_room', to='chat.room')),
                ('original_message', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='forwarded_messages_from', to='chat.message')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='forwarded_messages',
            field=models.ManyToManyField(blank=True, related_name='forwarded_to_messages', to='chat.forwardedmessage'),
        ),
    ]