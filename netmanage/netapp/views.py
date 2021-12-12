from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import validators
from .utils.xml_templates import loopback_ipv4_config, loopback_ipv6_config, loopback_delete_config
from .utils.connect import nc_connect, get_nc_connection_params, get_connection_params, cli_connect

from jinja2 import Template
import json


class ConfigureDeviceView(APIView):

    def post(self, request):

        content = json.loads(self.request.body)

        validation = validators.validate_api(content)
        if not validation["success"]:
            return Response(data=validation, status=status.HTTP_400_BAD_REQUEST)

        result, connection_params = get_nc_connection_params(content['host'])
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        if content['protocol'] == 'ipv4':
            tm = Template(loopback_ipv4_config)
        else:
            tm = Template(loopback_ipv6_config)

        payload = tm.render(loopbacks=content['loopbacks'])

        if content['dryrun'] in ['True', 1]:
            return Response(data=payload, status=status.HTTP_200_OK)

        result = nc_connect(connection_params, payload)
        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_201_CREATED)

    def delete(self, request):

        content = json.loads(self.request.body)

        validation = validators.validate_api(content)
        if not validation["success"]:
            return Response(data=validation, status=status.HTTP_400_BAD_REQUEST)

        result, connection_params = get_nc_connection_params(content['host'])
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        tm = Template(loopback_delete_config)
        payload = tm.render(loopbacks=content['loopbacks'])

        if content['dryrun'] in ['True', 1]:
            return Response(data=payload, status=status.HTTP_200_OK)

        result = nc_connect(connection_params, payload)
        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_200_OK)


class ListInterfacesView(APIView):

    def get(self, request):
        host = self.request.GET['host']

        result, connection_params, text_fsm_platform = get_connection_params(host)
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        command = "show ip interface brief"
        result = cli_connect(connection_params, command, text_fsm_platform)

        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_200_OK)