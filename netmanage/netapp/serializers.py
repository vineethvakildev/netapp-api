from rest_framework import serializers
from .models import AllDevices


class NetmikoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = ['host', 'device_type', 'username', 'password', 'secret', 'port']


class NetconfSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = ['host', 'device_params', 'username', 'password', 'port', 'hostkey_verify', 'allow_agent']
