from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from rest_framework.views import APIView
from .serializers import NetmikoSerializer, NetconfSerializer
from ntc_templates.parse import parse_output
from jinja2 import Template
from .utils.xml_templates import loopback_config, loopback_delete_config
from .utils.connect import nc_connect, get_connection_params
import json


class ListInterfacesView(APIView):

    def get(self, request):
        host = self.request.GET['host']
        queryset = AllDevices.objects.get(host__contains=host)
        device_details = NetmikoSerializer(queryset)

        try:
            net_connect = ConnectHandler(**device_details.data)
            output = net_connect.send_command('show ip interface brief')
        except Exception as err:
            exception_type = type(err).__name__

        interface_parsed = parse_output(platform=queryset.platform, command="show ip interface brief", data=output)

        return JsonResponse(interface_parsed, safe=False)


class ConfigureDeviceView(APIView):

    def post(self, request):

        content = json.loads(self.request.body)

        tm = Template(loopback_config)
        payload = tm.render(loopbacks=content['loopbacks'])

        connection_params = get_connection_params(content['host'])

        response = nc_connect(connection_params, payload)
        return response

    def delete(self, request):

        content = json.loads(self.request.body)

        tm = Template(loopback_delete_config)
        payload = tm.render(loopbacks=content['loopbacks'])

        connection_params = get_connection_params(content['host'])

        response = nc_connect(connection_params, payload)
        return response
