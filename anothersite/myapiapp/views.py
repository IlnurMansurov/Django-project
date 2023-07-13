from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from.serializers import GroupSerializer
from rest_framework.generics import GenericAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin



@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({'message':'Hello Wold!'})

class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #  return self.list(request)
       #groups = Group.objects.all()
       #serialized = GroupSerializer(groups, many=True)
        #return Response({'groups': serialized.data})


