from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

from users.models import UserExtended


@database_sync_to_async
def get_user(token):
    try:
        return UserExtended.objects.get(id=AccessToken(token)['user_id'])
    except Exception:
        return AnonymousUser()


class JwtAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]
        if token:
            scope["user"] = await get_user(token)
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
