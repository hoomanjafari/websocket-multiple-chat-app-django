import random

from django.db import models
from django.contrib.auth.models import User


def create_unique_code(length=10):
    src = 'abcdefghijklmnopqrstuvwxyz'
    unique_code = ''
    for i in range(length):
        unique_code += src[random.randint(0, len(src)) - 1]
    return unique_code


class ChatGroup(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_groups', verbose_name='Creator')
    title = models.CharField(max_length=66, verbose_name='Title')
    unique_code = models.CharField(max_length=10, default=create_unique_code, verbose_name='Unique code')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        verbose_name = 'Chat Group'
        verbose_name_plural = 'Chat Groups'

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members', verbose_name='User')
    chat_group = models.ForeignKey('ChatGroup', on_delete=models.CASCADE, related_name='members', verbose_name='Chat_Group')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f"{self.user} -- {self.chat_group}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='sender')
    chat_group = models.ForeignKey(
        'ChatGroup', on_delete=models.CASCADE, related_name='messages', verbose_name='Chat Group'
    )
    message = models.TextField(null=True, blank=True, verbose_name='Message')
    is_activity_msg = models.BooleanField(default=False, verbose_name='Activity Message')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f"{self.sender} -- {self.chat_group}"
