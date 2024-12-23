# Generated by Django 4.2 on 2024-12-16 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=66, verbose_name='Title')),
                ('unique_code', models.CharField(default='fssgetuteq', max_length=10, verbose_name='Unique code')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_groups', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name': 'Chat Group',
                'verbose_name_plural': 'Chat Groups',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Message')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chats.chatgroup', verbose_name='Chat Group')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('chat_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='chats.chatgroup', verbose_name='Chat Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
    ]
