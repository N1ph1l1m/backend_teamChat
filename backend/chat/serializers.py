from chat.models import Room, Message
from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer(many=True)

    class Meta:
        model = Message
        exlude = []
        fields = '__all__'
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")

class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    message = MessageSerializer(many = True, read_only = True)

    class Meta:
        model = Room
        fields = ["pk", "name", "host" , "message","current_users","last_message"]
        depth = 1
        read_only_fields = ["message", "last_message"]

    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.message.order_by('created_at').last()).data