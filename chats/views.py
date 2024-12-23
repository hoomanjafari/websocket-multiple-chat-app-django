from django.shortcuts import (render, redirect, get_object_or_404)
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, logout)
from django.views import View
from channels.consumer import get_channel_layer
from asgiref.sync import async_to_sync
# from django.utils.safestring import mark_safe

from .forms import (UserRegistrationForm, LoginForm, CreateGroupForm)
from .models import (ChatGroup, Member, Message)


# to display the main index
class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('chats:register')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # with this all chat groups that this user has been joined will display in index
        member = Member.objects.filter(user=request.user)
        return render(request, 'chats/index.html', {'member': member})


# to show the chat room that user has chosen
class ChatView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('chats:register')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        group_name = get_object_or_404(ChatGroup, unique_code=kwargs['unique_code'])
        try:
            Member.objects.get(user=request.user, chat_group=group_name)
            chat_group = get_object_or_404(ChatGroup, unique_code=kwargs['unique_code'])
            messages = Message.objects.filter(chat_group=chat_group)
            member = Member.objects.filter(user=request.user)
            return render(request, 'chats/chat.html', {
                'member': member, 'messages': messages, 'chat_group': chat_group,
            })
        # to redirect the client if it doesn't belong to chat room
        except Member.DoesNotExist:
            return redirect('chats:index')


# template for asking a client that has the invitation url, to join that room chat
class JoinChatView(View):
    def get(self, request, **kwargs):
        chat_group = get_object_or_404(ChatGroup, unique_code=kwargs['unique_code'])
        try:
            # if the client is already a member of that room chat just show him the chat template
            # otherwise ask him to if he wants to join
            Member.objects.get(user=request.user, chat_group=chat_group)
            return redirect('chats:chat-group', unique_code=kwargs['unique_code'])
        except Member.DoesNotExist:
            # this is the template for asking
            return render(request, 'chats/join_in.html', {
                'chat_group': chat_group,
            })

    def post(self, request, **kwargs):
        # this method is for that button in joining template to make the client as a member of this group
        chat_group = get_object_or_404(ChatGroup, unique_code=kwargs['unique_code'])
        Member.objects.create(
            user=request.user, chat_group=chat_group
        )
        Message.objects.create(
            sender=request.user, chat_group=chat_group, message='joined the group', is_activity_msg=True
        )
        # with this we send the message to that group that this new client is joined
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            kwargs['unique_code'],
            {
                'type': 'chat_message',
                'data': {
                    'message': 'member_joined',
                    'sender': request.user.username.capitalize(),
                    'activity_msg': True,
                }
            }
        )
        return redirect('chats:chat-group', unique_code=kwargs['unique_code'])


class LeaveChatView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('chats:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        chat_group = get_object_or_404(ChatGroup, unique_code=kwargs['unique_code'])
        get_object_or_404(Member, user=request.user, chat_group=chat_group).delete()
        channel_layer = get_channel_layer()
        # with this condition if the user is leaving the chat room is its owner than delete that chat room completely
        if chat_group.creator == request.user:
            chat_group.delete()
            # send alert to the members of that group that this group has been deleted by its owner
            async_to_sync(channel_layer.group_send)(
                kwargs['unique_code'],
                {
                    'type': 'chat_message',
                    'data': {
                        'message': 'group_deleted',
                        'sender': request.user.username.capitalize()
                    }
                }
            )
            return redirect('chats:index')
        # otherwise if the leaver is not the owner just make a message as this member is left and send it to the group
        Message.objects.create(
            sender=request.user, chat_group=chat_group, message='left the group', is_activity_msg=True
        )
        async_to_sync(channel_layer.group_send)(
            kwargs['unique_code'],
            {
                'type': 'chat_message',
                'data': {
                    'message': 'member_left',
                    'sender': request.user.username.capitalize(),
                    'activity_msg': True,
                }
            }
        )
        return redirect('chats:index')


# to create group chat and member
class CreateChatView(View):
    def post(self, request, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # making chat group
            gp = ChatGroup.objects.create(creator=request.user, title=cd['group_name'])
            # making the user as member of this group creator
            Member.objects.create(user=request.user, chat_group=gp)
            return redirect('chats:chat-group', gp.unique_code)
        member = Member.objects.filter(user=request.user)
        return render(request, 'chats/index.html', {'form': form, 'member': member})


class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chats:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'chats/register.html')

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password_confirm']
            )
            user = authenticate(username=cd['username'], password=cd['password_confirm'])
            if user is not None:
                login(request, user)
            return redirect('chats:index')
        return render(request, 'chats/register.html', {'form': form})


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('chats:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, 'chats/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('chats:index')
        return render(request, 'chats/login.html', {'form': form})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('chats:login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('chats:login')