from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

User = get_user_model()

class TokenAuthMiddleware:
    """
    Middleware для обработки TokenAuthentication в WebSocket.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Получение токена из URL
        query_string = parse_qs(scope['query_string'].decode())
        token_key = query_string.get('token', [None])[0]

        if token_key:
            # Получение пользователя из токена
            user = await self.get_user_from_token(token_key)
        else:
            user = AnonymousUser()

        scope['user'] = user
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()

# Оберните стандартный AuthMiddlewareStack
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
