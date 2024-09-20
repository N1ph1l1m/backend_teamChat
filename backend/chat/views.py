from asgiref.sync import sync_to_async
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from rest_framework import status
from chat import serializers
from .models import User, Room, Message
from rest_framework.views import APIView
from rest_framework.response import  Response


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

        other_user = User.objects.filter(username=other_user_username[0]).first()  # Получаем собеседника

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


def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'chat/room.html', {
        "room": room,
    })


def test(request):
    return render(request, 'chat/test.html')
