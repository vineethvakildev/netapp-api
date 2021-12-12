from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from rest_framework.views import APIView
from .serializers import NetmikoSerializer, NetconfSerializer
from jinja2 import Template
from .utils.xml_templates import loopback_config, loopback_delete_config
from .utils.connect import nc_connect, get_nc_connection_params, get_connection_params, cli_connect
import json


class ListInterfacesView(APIView):

    def get(self, request):

        host = self.request.GET['host']
        connection_params, text_fsm_platform = get_connection_params(host)

        command = "show ip interface brief"
        response = cli_connect(connection_params, command, text_fsm_platform)

        return response


class ConfigureDeviceView(APIView):

    def post(self, request):

        content = json.loads(self.request.body)

        tm = Template(loopback_config)
        payload = tm.render(loopbacks=content['loopbacks'])

        if content['dryrun']:
            return JsonResponse(data=payload, safe=False)

        connection_params = get_nc_connection_params(content['host'])

        response = nc_connect(connection_params, payload)
        return response

    def delete(self, request):

        content = json.loads(self.request.body)

        tm = Template(loopback_delete_config)
        payload = tm.render(loopbacks=content['loopbacks'])

        if content['dryrun']:
            return JsonResponse(data=payload, safe=False)

        connection_params = get_nc_connection_params(content['host'])

        response = nc_connect(connection_params, payload)
        return response
