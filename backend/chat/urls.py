from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.test , name='test'),
    path('room/<int:pk>',views.room,name = 'room'),
    path('index/', views.index, name ='index'),
    path('room/',views.RoomCreate.as_view()),
    path('roomg/',views.RoomGroupCreate.as_view()),
    path('rooms/',views.RoomListView.as_view(), name = 'roomList'),
    path('rooms/<int:pk>/',views.RoomDetailView.as_view()),
    path('room/message/',views.MessageListView.as_view()),
    path('photo-upload/', views.PhotoUploads.as_view()),
    path('docs/', views.DocumentsList.as_view()),
    path('documents-upload/', views.DocumentsUploads.as_view()),
    path('room/message/<int:pk>', views.MessageDetailView.as_view()),
    path('docs/<int:pk>/<str:filename>/',views.DocumentDetail.as_view()),
    # path('room/<int:pk>/create/message/', views.MessageViewSet.as_view({'post': 'create'})),
    # path('room/<int:id_room>/user/<str:sender_username>/message/', views.MessageViewSet.as_view({'post': 'create'})),

]