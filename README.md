# netapp-api
Netapp source code

**USER DOCUMENT**

**Overview**

Netapp REST APIs allows network engineers to manage their network devices over HTTP. Netapp API v1 is set of HTTP endpoints that help
users to confiure, unconfigure and monitor end devices. 

**Features**

Supports Ipv4 and IPv6 loopback configurations.
Includes dryrun feature to verify the Netconf payload without actually configuring the device.

**Endpoints**

*/api/configure*

This api uses Netconf - network management protocol to interact with Physical/Emulated devices.

The configure api has three uses:

1. Configure loopback intefaces. (HTTP Method: POST; Netconf Operation: Create)

2. Delete loopback interfaces. (HTTP Method: DELETE; Netconf Operation: Delete)

3. Generate payload using dryrun. (HTTP Method: POST)

URL STRUCTURE
http://127.0.0.1:8000/api/configure/

PARAMETERS                                              
{
    "loopbacks":[
        {
            "name": 5,
            "ip_add": "5000::1",
            "prefix": "128"
        },
        {
            "name": "6",
            "ip_add": "5000::2",
            "prefix": "128"
        }
    ],
    "host": "192.168.23.131",
    "dryrun": "False",
    "protocol": "ipv6"
}

RESPONSE

{
    "success": true,
    "errors": null,
    "details": "Configuration applied"
}

ERROR FORMAT

 { 
    "success": false,
    "errors": "RPCError",
    "details": "data-exists"
}

*/api/interfaces*

This api uses Netmiko to establish connectivity to the devices. 
The interfaces api can be used to:

Monitor the ipv4 interface status ((HTTP Method: GET)

URL STRUCTURE

http://127.0.0.1:8000/api/interfaces/?host=192.168.23.131

RESPONSE

{
    "success": true,
    "errors": null,
    "details": [
        {
            "intf": "MgmtEth0/0/CPU0/0",
            "ipaddr": "unassigned",
            "status": "Shutdown",
            "proto": "Down",
            "vrf": "default"
        },
        {
            "intf": "GigabitEthernet0/0/0/0",
            "ipaddr": "192.168.23.131",
            "status": "Up",
            "proto": "Up",
            "vrf": "default"
        }
    ]
}

ERROR FORMAT

{
    "success": false,
    "errors": "NetmikoTimeoutException",
    "details": "Unable to reach the device"
}


**DEVELOPER DOC**

_Framework_:                        _Libs for device management_:       _Templating_:
Django==3.2.10                      netmiko~=3.4.0                        Jinja2~=3.0.3
djangorestframework==3.12.4         ncclient~=0.6.12

**Components**

![image](https://user-images.githubusercontent.com/81028720/145894536-e5c407e0-c0da-4165-b413-97ad62aff40c.png)



*Build Docker container*

sudo docker build -t django-netapp .

sudo docker run -it -p 8020:8020 \
     -e DJANGO_SUPERUSER_USERNAME=admin \
     -e DJANGO_SUPERUSER_PASSWORD=vineeth \
     -e DJANGO_SUPERUSER_EMAIL=vineeth@uk.com \
     django-netapp











  
