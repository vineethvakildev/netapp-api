from ncclient.operations.rpc import RPCError
from ncclient.transport.errors import SessionCloseError, SSHError, SSHUnknownHostError
from ncclient import manager
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, SSHException
from ntc_templates.parse import parse_output


def nc_connect(connection_params, data):
    """

    :param connection_params:
    :param data:
    :return: result
    """
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
    """

    :param connection_params:
    :param command:
    :param text_fsm_platform:
    :return: result
    """
    result = {"success": True, "errors": None, "details": None}

    try:
        with ConnectHandler(**connection_params) as net_connect:
            output = net_connect.send_command(command)
            interface_parsed = parse_output(
                platform=text_fsm_platform, command=command, data=output
            )
            result["details"] = interface_parsed
    except (NetMikoTimeoutException, SSHException) as e:
        result["success"] = False
        result["details"] = "Unable to reach the device"
        result["errors"] = e.__class__.__name__
    except Exception as e:
        result["success"] = False
        result["details"] = "Unknown error"
        result["errors"] = e.__class__.__name__

    return result
