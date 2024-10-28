import json

from django.conf import settings
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from rest_framework import request

from .models import Room, Message, Photos , Documents
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer, RoomSerializer, UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer,  mixins.ListModelMixin):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    # @action()
    # async def create_message(self, message=None, image = None, **kwargs):
    #     room: Room = await self.get_room(pk=self.room_subscribe)
    #     await database_sync_to_async(Message.objects.create)(
    #         room=room,
    #         user=self.scope["user"],
    #         text=message,
    #         image = image,
    #     )

    # @action()
    # async def create_message(self, message=None, images=None, **kwargs):
    #     room: Room = await self.get_room(pk=self.room_subscribe)
    #     user = self.scope["user"]
    #
    #     # Проверка на дубликаты сообщений
    #     last_message = await database_sync_to_async(
    #         Message.objects.filter(room=room, user=user).order_by('-created_at').first
    #     )()
    #
    #     if last_message and last_message.text == message and last_message.images == images:
    #         # Сообщение уже создано
    #         return
    #
    #     # Создаем новое сообщение
    #     await database_sync_to_async(Message.objects.create)(
    #         room=room,
    #         user=user,
    #         text=message,
    #         images=images,
    #     )

    # @action()
    # async def create_message(self, message=None, images=None, **kwargs):
    #     room: Room = await self.get_room(pk=self.room_subscribe)
    #     user = self.scope["user"]
    #
    #     # Проверка на дубликаты сообщений
    #     last_message = await database_sync_to_async(
    #         Message.objects.filter(room=room, user=user).order_by('-created_at').first
    #     )()
    #
    #     if last_message and last_message.text == message and list(last_message.images.all()) == images:
    #         # Сообщение уже создано
    #         return
    #
    #     # Создаем новое сообщение без изображений
    #     new_message = await database_sync_to_async(Message.objects.create)(
    #         room=room,
    #         user=user,
    #         text=message,
    #     )
    #
    #     # Присоединяем изображения к сообщению
    #     if images:
    #         processed_images = []
    #         for img in images:
    #             # Находим объект Photos по изображению
    #             photo = await database_sync_to_async(Photos.objects.get)(image=img)
    #             processed_images.append(photo)
    #
    #         # Добавляем изображения к сообщению
    #         await database_sync_to_async(new_message.images.set)(processed_images)

    # @action()
    # async def create_message(self, message=None, images=None, **kwargs):
    #     room: Room = await self.get_room(pk=self.room_subscribe)
    #     user = self.scope["user"]
    #
    #     # Проверка на дубликаты сообщений
    #     last_message = await database_sync_to_async(
    #         Message.objects.filter(room=room, user=user).order_by('-created_at').first
    #     )()
    #
    #     if last_message:
    #         last_message_images = await database_sync_to_async(lambda: list(last_message.images.all()))()
    #         if last_message.text == message and last_message_images == images:
    #             # Сообщение уже создано
    #             return
    #
    #     # Создаем новое сообщение без изображений
    #     new_message = await database_sync_to_async(Message.objects.create)(
    #         room=room,
    #         user=user,
    #         text=message,
    #     )
    #
    #     # Добавляем изображения после создания сообщения
    #     if images:
    #         # Предполагаем, что 'images' - это список ID фотографий
    #         photos = await database_sync_to_async(Photos.objects.filter)(id__in=images)
    #         await database_sync_to_async(new_message.images.set)(photos)

    @action()
    async def create_message(self, message=None, images=None, documents = None ,  **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)
        user = self.scope["user"]

        # Проверка на дубликаты сообщений
        last_message = await database_sync_to_async(
            Message.objects.filter(room=room, user=user).order_by('-created_at').first
        )()

        if last_message:
            last_message_images = await database_sync_to_async(lambda: list(last_message.images.all()))()
            if last_message.text == message and last_message_images == images:
                return

        if last_message:
            last_message_documents = await database_sync_to_async(lambda: list(last_message.documents.all()))()
            if last_message.text == message and last_message_documents == documents:
                return

        # Создаем новое сообщение
        new_message = await database_sync_to_async(Message.objects.create)(
            room=room,
            user=user,
            text=message,
        )

        # Если есть изображения, добавляем их
        if images:
            # Предполагаем, что 'images' - это список ID фотографий
            photos = await database_sync_to_async(lambda: Photos.objects.filter(id__in=images))()
            await database_sync_to_async(new_message.images.set)(photos)

        if documents:
            # Предполагаем, что 'images' - это список ID фотографий
            document = await database_sync_to_async(lambda: Documents.objects.filter(id__in=documents))()
            await database_sync_to_async(new_message.documents.set)(document)

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.room_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: get_user_model = self.scope["user"]
        # user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: get_user_model = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))


class UserConsumer(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer,
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
