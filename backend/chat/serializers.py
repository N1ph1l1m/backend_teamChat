from chat.models import Room, Message, Photo
from django.contrib.auth import get_user_model
from users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username","photo"]
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user




class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']



class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id','image','upload_at']


class MessageSerializerCreate(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSer()
    photos = PhotoSerializer(many=True,read_only=True)
    image_files = serializers.ListField(child = serializers.ImageField(write_only = True), write_only = True)

    class Meta:
        model = Message
        exclude = []
        fields = ['id', 'room', 'text', 'user', 'created_at_formatted', 'photos', 'image_files']  # добавлено 'user'
        depth = 1
    def create(self, validated_data):
        image_files = validated_data.pop('image_files')
        message = Message.objects.create(**validated_data)
        for image_file in image_files:
            image = Photo.objects.create(file=image_file)
            message.images.add(image)
        return message

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")


#my
# class MessageSerializerCreate2(serializers.ModelSerializer):
#     created_at_formatted = serializers.SerializerMethodField()
#     user = UserSerializer()
#     photo = PhotoSerializer()
#
#     class Meta:
#         model = Message
#         exclude = []
#         field = ['user','photo', 'text' , 'created_at_formatted ']
#         depth = 1
#
#     def get_created_at_formatted(self, obj:Message):
#         return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")



class MessageSerializerCreate2(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        exlude = []
        fields = '__all__'
        #fields = ['user', 'text', 'image' ,'created_at_formatted']  # Все необходимые поля для сообщения
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        # Форматируем дату создания
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")



class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

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
    host = UserSerializer(read_only=True)
    current_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ["pk", "name", "host" , "current_users" ,"message","last_message"]
        depth = 1
        read_only_fields = ["message", "last_message"]

    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.message.order_by('created_at').last()).data



