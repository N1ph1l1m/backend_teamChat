from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'photo' , 'last_active')

class UserUpdateLastActivity(serializers.ModelSerializer):
    class Meta:
        model  = get_user_model()
        fields = ("id","last_active")