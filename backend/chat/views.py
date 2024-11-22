import os
from fileinput import filename

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, Http404, FileResponse
from rest_framework import status, viewsets
 # from .serializers import RoomSerializer, MessageSerializer , MessageSerializerCreate , PhotoSerializer
from .serializers import *
from rest_framework import generics
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from .models import  Room, Message, Photos , Documents  , ReactionToMessage
from rest_framework.views import APIView
import logging
logger = logging.getLogger(__name__)
from rest_framework.response import  Response
import urllib.parse
from urllib.parse import quote

def index(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:

            room = Room.objects.create(name=name, host=request.user)
            print(room)
            print(room.pk)
            print(name )
            print(request.user)
            return HttpResponseRedirect(reverse("room", kwargs={"pk": room.pk}))
    return render(request, 'chat/index.html')


class RoomCreate(APIView):
    def post(self, request):
        # Получаем текущего пользователя (хоста) и выбранного пользователя (собеседника)
        current_user = request.user
        other_user_username = request.data.get("current_users", [])  # Ожидается один пользователь

        if not other_user_username:
            return Response({"error": "Other user is required"}, status=status.HTTP_400_BAD_REQUEST)

        other_user = get_user_model().objects.filter(username=other_user_username[0]).first()  # Получаем собеседника

        if not other_user:
            return Response({"error": "Other user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Упорядочиваем пользователей для создания уникального имени комнаты
        sorted_users = sorted([current_user.username, other_user.username])
        room_name = f"{sorted_users[0]}_{sorted_users[1]}"  # Например, admin_user1 или user1_admin

        # Проверяем, существует ли уже комната с таким именем
        room = Room.objects.filter(name=room_name).first()

        if not room:
            # Если комната не найдена, создаем новую
            room = Room.objects.create(name=room_name, host=current_user)
            room.current_users.add(current_user, other_user)  # Добавляем обоих пользователей в комнату

            room_url = reverse("room", kwargs={"pk": room.pk})

            return Response({
                "pk": room.pk,
                "name": room.name,
                "current_users": [user.username for user in room.current_users.all()],
                "url": room_url
            }, status=status.HTTP_201_CREATED)
        else:
            # Если комната уже существует, возвращаем информацию о ней
            room_url = reverse("room", kwargs={"pk": room.pk})

            return Response({
                "pk": room.pk,
                "name": room.name,
                "current_users": [user.username for user in room.current_users.all()],
                "url": room_url
            }, status=status.HTTP_200_OK)


class RoomGroupCreate(APIView):
    def post(self, request):
        host_user = request.user
        other_user_usernames = request.data.get("current_users")
        room_name = request.data.get("name")

        # Проверка на пустое имя хоста
        if not host_user.username:
            return Response({"error": "Имя хоста не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на пустое имя комнаты
        if not room_name:
            return Response({"error": "Имя комнаты не может быть пустым"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на пустой список пользователей
        if not other_user_usernames:
            return Response({"error": "Необходимо указать хотя бы одного другого пользователя"}, status=status.HTTP_400_BAD_REQUEST)

        # Находим других пользователей по их именам
        other_users = get_user_model().objects.filter(username__in=other_user_usernames)

        if not other_users.exists():
            return Response({"error": "Другие пользователи не найдены"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, существует ли комната с таким именем
        room = Room.objects.filter(name=room_name).first()

        if not room:
            # Если комната не найдена, создаем новую
            room = Room.objects.create(host=host_user, name=room_name)

            # Добавляем текущего пользователя и других пользователей в комнату
            room.current_users.add(host_user)
            room.current_users.add(*other_users)

            room_url = reverse("room", kwargs={"pk": room.pk})

            return Response({
                "pk": room.pk,
                "name": room.name,
                "current_users": [user.username for user in room.current_users.all()],
                "url": room_url
            }, status=status.HTTP_201_CREATED)
        else:
            # Если комната уже существует, возвращаем информацию о ней
            room_url = reverse("room", kwargs={"pk": room.pk})

            return Response({
                "pk": room.pk,
                "name": room.name,
                "current_users": [user.username for user in room.current_users.all()],
                "url": room_url
            }, status=status.HTTP_200_OK)
class  RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class  = RoomSerializer

class RoomDetailView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class DocumentDetail(APIView):
    def get(self, request, pk, filename, *args, **kwargs):
        try:
            # Получаем объект документа
            document = Documents.objects.get(pk=pk)
            file_path = document.document.path  # Путь к файлу

            # Проверяем, существует ли файл
            if not os.path.exists(file_path):
                raise Http404("Файл не найден")

            # Кодируем имя файла для поддержки русских символов
            encoded_filename = quote(filename)

            # Создаем ответ с файлом
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            response['Content-Type'] = 'application/octet-stream'

            return response

        except Documents.DoesNotExist:
            raise Http404("Документ не найден")


class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# class MessageUpdateReactions(generics.UpdateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageUpdateSerializer


# class MessageUpdateReactions(generics.UpdateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageUpdateSerializer
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#
#         # Обновляем поле reactions через метод add()
#         reactions_data = request.data.get("reactions", [])
#         for reaction_id in reactions_data:
#             reaction_instance = ReactionToMessage.objects.get(id=reaction_id["id"])
#             instance.reactions.add(reaction_instance)
#
#         instance.save()
#
#         return Response(serializer.data)


class MessageUpdateReactions(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Получаем реакции из запроса
        reaction_ids = request.data.get("reactions", [])
        for reaction_id in reaction_ids:
            try:
                reaction_instance = ReactionToMessage.objects.get(id=reaction_id)

                # Проверяем, есть ли у этого пользователя реакция в сообщении
                existing_reaction = instance.reactions.filter(id_user=reaction_instance.id_user).first()
                if existing_reaction:
                    # Удаляем старую реакцию
                    instance.reactions.remove(existing_reaction)

                # Добавляем новую реакцию
                instance.reactions.add(reaction_instance)
            except ReactionToMessage.DoesNotExist:
                return Response({"error": f"Reaction with id {reaction_id} does not exist."}, status=400)

        instance.save()

        # Сериализуем обновленное сообщение
        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data)


class PhotoDetailView(generics.RetrieveAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer

class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ReactionToMessageCreateView(generics.CreateAPIView):
    queryset = ReactionToMessage.objects.all()
    serializer_class = ReactionToMessageCreateSerializer

class ReactionToMessageListView(generics.ListAPIView):
    queryset = ReactionToMessage.objects.all()
    serializer_class = ReactionToMessageSerializer

class ReactionToMessageRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReactionToMessage.objects.all()
    serializer_class = ReactionToMessageSerializer



class PhotoUploads(generics.CreateAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializer


class DocumentsUploads(generics.CreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer

class DocumentsList(generics.ListAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializerCreate2

    def create(self, request, id_room, sender_username, *args, **kwargs):
        room = get_object_or_404(Room, pk=id_room)
        user = get_object_or_404(get_user_model(), username=sender_username)

        # Получаем текст сообщения
        text = request.data.get('text', '')

        # Получаем список идентификаторов изображений
        image_ids = request.data.get('image', [])
        if isinstance(image_ids, str):
            image_ids = image_ids.split(',')  # Преобразуем строку в список, если это необходимо

        # Создаем сообщение
        message = Message.objects.create(room=room, user=user, text=text)

        # Если есть изображения, связываем их с сообщением
        if image_ids:
            photos = Photos.objects.filter(id__in=image_ids)  # Получаем все изображения по id
            message.images.set(photos)  # Используем set для ManyToMany отношения

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'chat/room.html', {
        "room": room,
    })


def test(request):
    return render(request, 'chat/test.html')
