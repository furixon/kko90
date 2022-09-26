from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
# Create your views here.


def index(request):
    return HttpResponse('Hello')


class KkoMsgViewSet(viewsets.ModelViewSet):
    """
    kkomsg - 카카오톡 메시지 전송 요청 API
    ---
    
    """
    queryset = KkoMsg.objects.all()
    serializer_class = KkoMsgSerializer
    permission_classes = [HasAPIKey | IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head']
    # lookup_field = "client_id"

    def create(self, request, *args, **kwargs):
        response = super(KkoMsgViewSet, self).create(request, *args, **kwargs)
        instance = response.data
        instance['success'] = 'Data successfully submitted'

        return Response(instance, status=status.HTTP_201_CREATED)


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

    swagger_schema = None


class MsgTemplateViewSet(viewsets.ModelViewSet):
    queryset = MsgTemplate.objects.all()
    serializer_class = MsgTemplateSerializer


class PrivateKkoMsgViewSet(viewsets.ModelViewSet):
    queryset = KkoMsg.objects.all()
    serializer_class = KkoMsgSerializer
    # permission_classes = [HasAPIKey | IsAuthenticated]

    swagger_schema = None
