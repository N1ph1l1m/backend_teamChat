from chat.models import Room, Message, Photos , Documents , ReactionToMessage , ForwardedMessage
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
        fields = ['id','username' , "photo"]



class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['id','image','upload_at']

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['id','document', 'name' , 'upload_at']


class MultiplePhotoSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField())


class MultipleDocumentSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.FileField())


class MessageSerializerCreate2(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'
        #fields = ['user', 'text', 'image' ,'created_at_formatted']  # Все необходимые поля для сообщения
        depth = 1

    def get_created_at_formatted(self, obj: Message):
        # Форматируем дату создания
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")


class ReplyToSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Пользователь, написавший ответ
    images = PhotoSerializer(many=True)  # Сериализуем все связанные изображения
    documents = DocumentsSerializer(many=True)  # Сериализуем все связанные документы

    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at', 'user', 'images', 'documents']  # Только необходимые поля


class UserReactionSererializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username" , "photo"]

class ReactionToMessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReactionToMessage
        fields = ['id', 'emoji', 'id_user']

class ReactionToMessageSerializer(serializers.ModelSerializer):
    id_user = UserReactionSererializer()
    class Meta:
        model = ReactionToMessage
        fields = ['id', 'emoji', 'id_user']


class MessageSerializer2(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()
    images = PhotoSerializer(many=True)
    documents = DocumentsSerializer(many=True)
    reply_to = ReplyToSerializer()
    reactions = ReactionToMessageSerializer(many=True)
    # forwarded_messages = ForwardedMessageSerializer(many=True)

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")


class ForwardedCreate(serializers.ModelSerializer):
    class Meta:
        model = ForwardedMessage
        fields = '__all__'

class ForwardedMessageSerializer(serializers.ModelSerializer):
    original_message = MessageSerializer2()
    #forwarded_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    forwarded_by = UserSerializer()
    forwarded_to_room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    forwarded_at = serializers.DateTimeField()

    class Meta:
        model = ForwardedMessage
        fields = ['id', 'original_message', 'forwarded_by', 'forwarded_to_room', 'forwarded_at']


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()
    images = PhotoSerializer(many=True)
    documents = DocumentsSerializer(many=True)
    reply_to = ReplyToSerializer()
    reactions = ReactionToMessageSerializer(many=True)
    forwarded_messages = ForwardedMessageSerializer(many=True)

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")


class CreateMessageSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(
         queryset=Room.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
         queryset=User.objects.all())
    forwarded_messages = serializers.PrimaryKeyRelatedField(many=True,
         queryset=ForwardedMessage.objects.all())

    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['room', 'user','forwarded_messages' , 'created_at_formatted' , 'text']
        depth = 1

    def get_created_at_formatted(self, obj:Message):
        return obj.created_at.strftime("%d-%m-%Y  %H:%M:%S")


# class MessageUpdateSerializer(serializers.ModelSerializer):
#     created_at_formatted = None  # Удаляем это поле из серилизатора
#     class Meta:
#         model = Message
#         exclude = ["user", "images", "reply_to", "room", "documents", "text", "created_at"]
#         depth = 1

class MessageUpdateSerializer(serializers.ModelSerializer):
    reactions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=ReactionToMessage.objects.all()
    )

    class Meta:
        model = Message
        fields = ['id', 'reactions']


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    message = MessageSerializer(many = True, read_only = True)
    host = UserSerializer(read_only=True)
    current_users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ["pk", "name",  "photo_room" , "host" , "current_users" ,"message","last_message"]
        depth = 1
        read_only_fields = ["message", "last_message"]

    def get_last_message(self, obj:Room):
        return MessageSerializer(obj.message.order_by('created_at').last()).data



