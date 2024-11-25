import json

from django.conf import settings
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from rest_framework import request

from .models import Room, Message, Photos , Documents , ReactionToMessage
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer, RoomSerializer, UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer,  mixins.ListModelMixin  , mixins.UpdateModelMixin):
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



    @action()
    async def create_message(self, message=None, images=None, documents=None, reply_to=None, **kwargs):
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

            last_message_documents = await database_sync_to_async(lambda: list(last_message.documents.all()))()
            if last_message.text == message and last_message_documents == documents:
                return

        # Проверка существования родительского сообщения, если передан reply_to
        parent_message = None
        if reply_to:
            parent_message = await database_sync_to_async(Message.objects.filter(id=reply_to).first)()
            if not parent_message:
                # Обработка случая, если указанного сообщения не существует
                return {"error": "Parent message not found"}

        # Создаем новое сообщение
        new_message = await database_sync_to_async(Message.objects.create)(
            room=room,
            user=user,
            text=message,
            reply_to=parent_message,  # Указываем родительское сообщение
        )

        # Если есть изображения, добавляем их
        if images:
            # Предполагаем, что 'images' - это список ID фотографий
            photos = await database_sync_to_async(lambda: Photos.objects.filter(id__in=images))()
            await database_sync_to_async(new_message.images.set)(photos)

        # Если есть документы, добавляем их
        if documents:
            # Предполагаем, что 'documents' - это список ID документов
            docs = await database_sync_to_async(lambda: Documents.objects.filter(id__in=documents))()
            await database_sync_to_async(new_message.documents.set)(docs)



        # Возвращаем информацию о созданном сообщении
        return {
            "message_id": new_message.id,
            "text": new_message.text,
            "reply_to": new_message.reply_to.id if new_message.reply_to else None,
            "user": new_message.user.username,
            "room": new_message.room.name,
            "created_at": new_message.created_at.isoformat(),
        }

    @action()
    async def update_message_reactions(self, message_id=None, reaction_id=None, **kwargs):
        user = self.scope["user"]
        room: Room = await self.get_room(pk=self.room_subscribe)

        # Проверяем, существует ли сообщение
        existing_message = await database_sync_to_async(Message.objects.filter(id=message_id, room=room).first)()
        if not existing_message:
            return {"error": "Message not found"}

        # Получаем реакцию из базы данных
        reaction = await database_sync_to_async(ReactionToMessage.objects.filter(id=reaction_id).first)()
        if not reaction:
            return {"error": "Reaction not found"}

        # Проверяем, существует ли уже реакция от текущего пользователя
        existing_reaction = await database_sync_to_async(existing_message.reactions.filter(id_user=user).first)()
        if existing_reaction:
            # Удаляем старую реакцию
            await database_sync_to_async(existing_message.reactions.remove)(existing_reaction)

        # Добавляем новую реакцию
        await database_sync_to_async(existing_message.reactions.add)(reaction)

        # Сохраняем изменения
        await database_sync_to_async(existing_message.save)()

        # Получаем все реакции
        reactions = await database_sync_to_async(lambda: list(existing_message.reactions.all()))()

        # Формируем список реакций
        reaction_list = []
        for r in reactions:
            username = await database_sync_to_async(lambda: r.id_user.username)()
            reaction_list.append({"reaction_id": r.id, "user": username})

        # Возвращаем обновлённое сообщение
        return {
            "message_id": existing_message.id,
            "reactions": reaction_list,
            "created_at": existing_message.created_at.isoformat(),  # Используем существующее поле
        }

    @action()
    async def delete_reaction(self, message_id=None, reaction_id=None, **kwargs):
        user = self.scope["user"]  # Получаем текущего пользователя
        room = await self.get_room(pk=self.room_subscribe)  # Получаем комнату

        # Проверяем, существует ли сообщение
        message = await sync_to_async(Message.objects.filter(id=message_id, room=room).first)()
        if not message:
            return {"error": "Message not found"}

        # Проверяем, существует ли реакция
        reaction = await sync_to_async(ReactionToMessage.objects.filter(id=reaction_id).first)()
        if not reaction:
            return {"error": "Reaction not found"}

        # Удаляем реакцию из сообщения
        await sync_to_async(message.reactions.remove)(reaction)

        # Сохраняем изменения
        await sync_to_async(message.save)()

        # Получаем обновлённый список реакций
        reactions = await sync_to_async(lambda: list(message.reactions.all()))()

        # Формируем список обновленных реакций
        reaction_list = []
        for r in reactions:
            username = await sync_to_async(lambda: r.id_user.username)()
            reaction_list.append({
                "reaction_id": r.id,
                "emoji": r.emoji,
                "user": username
            })

        # Возвращаем обновлённые данные о сообщении
        return {
            "message_id": message.id,
            "reactions": reaction_list,
            "created_at": message.created_at.isoformat(),
        }



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

class MessageConsumer(mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.PatchModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        mixins.DeleteModelMixin,
        GenericAsyncAPIConsumer):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer