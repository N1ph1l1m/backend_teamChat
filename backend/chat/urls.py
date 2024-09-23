from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.test , name='test'),
    path('room/<int:pk>',views.room,name = 'room'),
    path('index/', views.index, name ='index'),
    path('room/',views.RoomCreate.as_view()),
    path('rooms/',views.RoomListView.as_view(), name = 'roomList'),
    path('rooms/<int:pk>/',views.RoomDetailView.as_view()),
    path('room/message/',views.MessageListView.as_view()),
    path('room/message/<int:pk>', views.MessageDetailView.as_view()),

]
