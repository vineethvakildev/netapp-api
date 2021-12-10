from rest_framework import serializers
from .models import AllDevices


class AllDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllDevices
        fields = '__all__'
