"""
ASGI config for multiple_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import (ProtocolTypeRouter, URLRouter)
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chats import routing as chats_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiple_chat.settings')

django_asgi_application = get_asgi_application()


# this works like the main url that we include other apps urls in it
application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(chats_routing.websocket_urlpatterns)
            )
        )
    )
})
