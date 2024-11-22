from django.urls import path, re_path

from . import consumers


websocket_urlpatterns = [
    path("ws/", consumers.UserConsumer.as_asgi()),
    path('ws/chat/', consumers.RoomConsumer.as_asgi()),
    path('ws/message/',consumers.MessageConsumer.as_asgi()),
    path('ws/message/<int:pk>/', consumers.MessageConsumer.as_asgi()),
    path("ws/chat/<int:room_id>/", consumers.RoomConsumer.as_asgi()),
]
