from django.urls import path, re_path

from . import consumers


websocket_urlpatterns = [
    path("ws/", consumers.UserConsumer.as_asgi()),
    path('ws/chat/', consumers.RoomConsumer.as_asgi()),
    # #re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.RoomConsumer.as_asgi()),
    # re_path(r"ws/chat/(?P<room_name>\d+)/$", consumers.RoomConsumer.as_asgi()),  # \d+ для чисел
    #path("ws/chat/<int:room_id>/", consumers.RoomConsumer.as_asgi()),
    #re_path(r'ws/chat/room/$', consumers.RoomConsumer.as_asgi()),
]
