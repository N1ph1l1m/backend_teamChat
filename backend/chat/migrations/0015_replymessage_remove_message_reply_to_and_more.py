# Generated by Django 5.1.1 on 2024-11-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_message_reply_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_message', models.CharField(blank=True, max_length=255)),
                ('name_parent', models.CharField(blank=True, max_length=255)),
                ('text_message', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='reply_to',
        ),
        migrations.AddField(
            model_name='message',
            name='reply_message',
            field=models.ManyToManyField(related_name='reply_message', to='chat.replymessage'),
        ),
    ]
