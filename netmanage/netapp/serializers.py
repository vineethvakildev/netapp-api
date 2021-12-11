from rest_framework import serializers
from .models import AllDevices


class NetmikoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = ['ip', 'device_type', 'username', 'password', 'secret', 'port']
