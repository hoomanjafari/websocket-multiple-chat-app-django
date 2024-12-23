from django.contrib import admin
from . models import (ChatGroup, Member, Message)


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ['creator', 'title', 'created_at']
    search_fields = ['creator', 'title']
    list_filter = ['unique_code']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat_group', 'created_at']
    search_fields = ['user', 'chat_group']
    list_filter = ['user', 'chat_group', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'chat_group', 'created_at']
    search_fields = ['sender', 'chat_group']
    list_filter = ['sender', 'chat_group', 'created_at']
