from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import SessionCloseError, SSHError, SSHUnknownHostError
from ncclient import manager
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, SSHException
from ntc_templates.parse import parse_output

from ..models import AllDevices
from ..serializers import NetmikoSerializer, NetconfSerializer


def get_connection_params(host):
    result = {"success": True, "errors": None, "details": None}
    connection_params = None
    text_fsm_platform = None
    try:
        queryset = AllDevices.objects.get(host__iexact=host)
        text_fsm_platform = queryset.platform
        device_details = NetmikoSerializer(queryset)
        connection_params = device_details.data
    except Exception as e:
        result["success"] = False
        result["details"] = "Invalid host"
        result["errors"] = e.__class__.__name__

    return result, connection_params, text_fsm_platform


def get_nc_connection_params(host):
    result = {"success": True, "errors": None, "details": None}
    connection_params = None

    try:
        queryset = AllDevices.objects.get(host__iexact=host)
        device_details = NetconfSerializer(queryset)
        connection_params = device_details.data
        connection_params['device_params'] = {'name': queryset.device_params}
    except Exception as e:
        result["success"] = False
        result["details"] = "Invalid host"
        result["errors"] = e.__class__.__name__

    return result, connection_params


def nc_connect(connection_params, data):
    result = {"success": True, "errors": None, "details": "Configuration applied"}

    try:
        with manager.connect(**connection_params) as m:
            nc_reply = m.edit_config(data, target="candidate")
            if nc_reply.ok:
                nc_reply = m.commit()
                if not nc_reply.ok:
                    result["success"] = False
                    result["details"] = "Configuration commit failed"
            else:
                result["success"] = False
                result["details"] = "Configuration apply failed"

    except (RPCError, SessionCloseError, SSHError, SSHUnknownHostError) as e:
        result["success"] = False
        result["details"] = e.tag
        result["errors"] = e.__class__.__name__
    except Exception as e:
        result["success"] = False
        result["details"] = "Unknown error"
        result["errors"] = e.__class__.__name__

    return result


def cli_connect(connection_params, command, text_fsm_platform):
    result = {"success": True, "errors": None, "details": None}

    try:
        net_connect = ConnectHandler(**connection_params)
        output = net_connect.send_command(command)
        interface_parsed = parse_output(platform=text_fsm_platform, command=command, data=output)
        result["details"] = interface_parsed
    except (NetMikoTimeoutException, SSHException) as e:
        result["success"] = False
        result["details"] = e.tag
        result["errors"] = e.__class__.__name__
    except Exception as e:
        result["success"] = False
        result["details"] = "Unknown error"
        result["errors"] = e.__class__.__name__

    return result
