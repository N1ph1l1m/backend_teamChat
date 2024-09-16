from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.test , name='test'),
    path('room/<int:pk>',views.room,name = 'room'),
    path('', views.index, name ='index'),
]
