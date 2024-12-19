

from djangochannelsrestframework import mixins
from .models import Room
from .serializers import MessageSerializer, RoomSerializer, UserSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

class RoomListConsumer(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DeleteModelMixin,
                       GenericAsyncAPIConsumer):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

