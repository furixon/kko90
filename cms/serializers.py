from rest_framework import serializers
from .models import *


class KkoMsgSerializer(serializers.ModelSerializer):

    class Meta:
    	model = KkoMsg
    	fields = ('id', 'agency_name', 'client_name', 'msg_index', 'client_id', 'kko_url')


class AgencySerializer(serializers.ModelSerializer):

    class Meta:
    	model = Agency
    	fields = '__all__'


class MsgTemplateSerializer(serializers.ModelSerializer):

    class Meta:
    	model = MsgTemplate
    	fields = '__all__'
