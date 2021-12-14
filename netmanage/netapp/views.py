from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from . import validators
from .utils import connect
from .utils import params
from .utils import loopback_templates as tmpl
from jinja2 import Template
import json


class ConfigureDeviceView(APIView):

    def post(self, request):

        content = json.loads(self.request.body)

        # validate user input
        validation = validators.validate_api(content)
        if not validation["success"]:
            return Response(data=validation, status=status.HTTP_400_BAD_REQUEST)

        # get the connection parameters required for netconf client lib
        result, connection_params = params.get_nc_connection_params(content["host"])
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        # render xml template based on ip protocol
        if content["protocol"] == "ipv4":
            tm = Template(tmpl.LOOPBACK_IPV4_CONFIG)
        else:
            tm = Template(tmpl.LOOPBACK_IPV6_CONFIG)

        payload = tm.render(loopbacks=content["loopbacks"])

        if content["dryrun"] in ["True", 1]:
            return Response(data=payload, status=status.HTTP_200_OK)

        # connect and send data to the device
        result = connect.nc_connect(connection_params, payload)
        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_201_CREATED)

    def delete(self, request):

        content = json.loads(self.request.body)

        # validate user input
        validation = validators.validate_api(content)
        if not validation["success"]:
            return Response(data=validation, status=status.HTTP_400_BAD_REQUEST)

        # get the connection parameters required for netconf client lib
        result, connection_params = params.get_nc_connection_params(content["host"])
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        tm = Template(tmpl.LOOPBACK_DELETE_CONFIG)
        payload = tm.render(loopbacks=content["loopbacks"])

        if content["dryrun"] in ["True", 1]:
            return Response(data=payload, status=status.HTTP_200_OK)

        # connect and send data to the device
        result = connect.nc_connect(connection_params, payload)
        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_200_OK)


class ListInterfacesView(APIView):
    def get(self, request):
        host = self.request.GET.get("host")

        # get the connection parameters required for ssh client lib
        result, connection_params, text_fsm_platform = params.get_connection_params(
            host
        )
        if not result["success"]:
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

        # connect to device and send command
        command = "show ip interface brief"
        result = connect.cli_connect(connection_params, command, text_fsm_platform)

        if not result["success"]:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=result, status=status.HTTP_200_OK)
