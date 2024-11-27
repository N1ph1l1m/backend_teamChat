# Generated by Django 5.1.1 on 2024-11-27 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_alter_message_reactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='forwarded_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forwarded_messages', to='chat.message'),
        ),
    ]
