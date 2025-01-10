from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, viewsets

from .serializers import UserSerializer , UserUpdateLastActivity

class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UpdateLastActivity(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserUpdateLastActivity

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UsersListSerializer
