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
    except AllDevices.DoesNotExist as e:
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
        connection_params["device_params"] = {"name": queryset.device_params}
    except AllDevices.DoesNotExist as e:
        result["success"] = False
        result["details"] = "Invalid host"
        result["errors"] = e.__class__.__name__

    return result, connection_params
