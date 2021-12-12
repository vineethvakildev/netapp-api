from rest_framework.response import Response
from rest_framework import status

from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import SessionCloseError, SSHError, SSHUnknownHostError
from ncclient import manager
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from ntc_templates.parse import parse_output

from ..models import AllDevices
from ..serializers import NetmikoSerializer, NetconfSerializer


def get_connection_params(host):
    queryset = AllDevices.objects.get(host__iexact=host)
    device_details = NetmikoSerializer(queryset)
    connection_params = device_details.data
    return connection_params, queryset.platform


def get_nc_connection_params(host):
    queryset = AllDevices.objects.get(host__iexact=host)
    device_details = NetconfSerializer(queryset)
    connection_params = device_details.data
    connection_params['device_params'] = {'name': queryset.device_params}
    return connection_params


def nc_connect(connection_params, data):

    try:
        with manager.connect(**connection_params) as m:
            nc_reply = m.edit_config(data, target="candidate")
            nc_reply = m.commit()

            if nc_reply.ok:
                message = "Success"
                code = status.HTTP_200_OK
    except RPCError as e:
        message = e.__class__.__name__
        code = status.HTTP_400_BAD_REQUEST
    except (SessionCloseError, SSHError, SSHUnknownHostError) as e:
        message = e.__class__.__name__
        code = status.HTTP_503_SERVICE_UNAVAILABLE
    except Exception as e:
        message = e.__class__.__name__
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        response = Response(data={
            "message": message
        }, status=code)

        return response


def cli_connect(connection_params, command, text_fsm_platform):

    interface_parsed = {}
    try:
        net_connect = ConnectHandler(**connection_params)
        output = net_connect.send_command(command)
        interface_parsed = parse_output(platform=text_fsm_platform, command=command, data=output)
        message = "Success"
        code = status.HTTP_200_OK
    except (NetMikoTimeoutException, SSHException) as e:
        message = e.__class__.__name__
        code = status.HTTP_503_SERVICE_UNAVAILABLE
    except Exception as e:
        message = e.__class__.__name__
        code = status.HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        response = Response(data={
            "message": message,
            "interfaces": interface_parsed
        }, status=code)
        return response
