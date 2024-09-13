import django
from django.urls import path
from django.urls import  include
from . import views

# router = routers.Simple


urlpatterns =[
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]