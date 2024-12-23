from django.urls import path
from . import views


app_name = 'chats'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('chat-group/<str:unique_code>/', views.ChatView.as_view(), name='chat-group'),
    path('create-group/', views.CreateChatView.as_view(), name='group-create'),
    path('join-chat/<str:unique_code>/', views.JoinChatView.as_view(), name='join-chat'),
    path('leave-chat/<str:unique_code>/', views.LeaveChatView.as_view(), name='leave-chat'),
]
