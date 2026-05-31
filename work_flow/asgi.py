"""
ASGI config for work_flow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from notifications.jwt_middleware import JwtAuthMiddleware
from notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'work_flow.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": JwtAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
