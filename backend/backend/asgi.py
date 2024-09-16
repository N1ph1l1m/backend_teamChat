"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from backend.chat import routing


from chat.middleware import JwtAuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# from chat import routing
#django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":JwtAuthMiddlewareStack(
        URLRouter(
            routing.webSocket_urlpatterns
        )
    )
})
