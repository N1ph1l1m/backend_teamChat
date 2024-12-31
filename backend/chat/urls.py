from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.test , name='test'),
    path('room/<int:pk>',views.room,name = 'room'),
    path('index/', views.index, name ='index'),
    path('room/',views.RoomCreate.as_view()),
    path('create-groupchat/',views.RoomGroupCreate.as_view()),
    path('rooms/',views.RoomListView.as_view(), name = 'roomList'),
    path('rooms/<int:pk>/',views.RoomDetailView.as_view()),
    path('room/message/',views.MessageListView.as_view()),
    path('photo-upload/', views.PhotoUploads.as_view()),
    path('docs/', views.DocumentsList.as_view()),
    path('message-update/<int:pk>/',views.MessageUpdateReactions.as_view()),
    path('message/<int:pk>/',views.MessageDetail.as_view()),
    path('message-create/',views.MessageCreate.as_view()),
    path('message-read/<int:pk>/',views.MessageUpdateReadMessage.as_view()),
    path("message-read-status/<int:user_id>/",views.MessageCheckRead.as_view()),
    path('message-read-all/<int:user_id>/',views.MessageReadAll.as_view()),
    path('photo/<int:pk>/', views.PhotoDetailView.as_view()),
    path('reaction/',views.ReactionToMessageCreateView.as_view()),
    path('reaction/destroy/<int:pk>/',views.ReactionToMessageDeleteView.as_view()),
    path('reaction/<int:pk>', views.ReactionToMessageRetrieveView.as_view()),
    path('reaction-list/', views.ReactionToMessageListView.as_view()),
    path('documents-upload/', views.DocumentsUploads.as_view()),
    path('room/message/<int:pk>', views.MessageDetailView.as_view()),
    # path("forward/",views.ForwardMessagesView.as_view()),
    path("forward-create/",views.ForwardMessageCreate.as_view()),
    path("forward-list/", views.ForwardMessagesList.as_view()),
    path("forward/<int:pk>/", views.ForwardMessagesDetail.as_view()),
    path('docs/<int:pk>/<str:filename>/',views.DocumentDetail.as_view()),
    path("tokens/",views.TokenCheck.as_view()),
    # path('room/<int:pk>/create/message/', views.MessageViewSet.as_view({'post': 'create'})),
    # path('room/<int:id_room>/user/<str:sender_username>/message/', views.MessageViewSet.as_view({'post': 'create'})),

]