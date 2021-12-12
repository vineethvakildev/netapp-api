from rest_framework import serializers
from .models import AllDevices


class NestedSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    ip_add = serializers.IPAddressField(required=True)
    prefix = serializers.CharField(required=True)


class DataSerializer(serializers.Serializer):
    loopbacks = serializers.ListSerializer(child=NestedSerializer())
    host = serializers.IPAddressField(required=True)
    dryrun = serializers.BooleanField(required=True)
    protocol = serializers.ChoiceField(required=True, choices=['ipv4', 'ipv6'])


class NetmikoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = ['host', 'device_type', 'username', 'password', 'secret', 'port']


class NetconfSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = ['host', 'device_params', 'username', 'password', 'port', 'hostkey_verify', 'allow_agent']
