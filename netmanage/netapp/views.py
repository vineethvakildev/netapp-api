from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException
from .serializers import NetmikoSerializer
from .models import AllDevices
from ntc_templates.parse import parse_output


class ListInterfacesView(View):

    def get(self, request):
        ip = self.request.GET['ip']
        queryset = AllDevices.objects.get(ip__contains=ip)
        device_details = NetmikoSerializer(queryset)

        try:
            net_connect = ConnectHandler(**device_details.data)
            output = net_connect.send_command('show ip interface brief')
        except Exception as err:
            exception_type = type(err).__name__

        interface_parsed = parse_output(platform=queryset.platform, command="show ip interface brief", data=output)

        return JsonResponse(interface_parsed, safe=False)


