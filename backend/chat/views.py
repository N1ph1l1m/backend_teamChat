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
        name = request.data.get("name")
        current_users = request.data.get("current_users", [])  # Получаем текущих пользователей, если есть
        # Проверяем наличие имени
        if name:
            if  not Room.objects.filter(name=name).first():
                # Создаем новую комнату
                room = Room.objects.create(name=name, host=request.user)

                # Добавляем текущих пользователей в комнату, если они существуют
                for username in current_users:
                    user = User.objects.filter(username=username).first()  # Получаем пользователя по имени
                    if user:
                        room.current_users.add(user)  # Добавляем пользователя в current_users

                # Подготовка ссылки на созданную комнату
                room_url = reverse("room", kwargs={"pk": room.pk})

                # Возвращаем данные о созданной комнате и ссылку
                return Response({
                    "pk": room.pk,
                    "name": room.name,
                    "current_users": [user.username for user in room.current_users.all()],  # Возвращаем список пользователей
                    "url": room_url
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Room with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)







def room(request, pk):
    room: Room = get_object_or_404(Room, pk=pk)
    return render(request, 'chat/room.html', {
        "room": room,
    })


def test(request):
    return render(request, 'chat/test.html')
