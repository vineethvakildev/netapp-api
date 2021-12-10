from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .serializers import AllDevicesSerializer


class ConfigureDeviceView(View):

    def get(self, request):
        # <view logic>
        return HttpResponse('result')

# Create your views here.


