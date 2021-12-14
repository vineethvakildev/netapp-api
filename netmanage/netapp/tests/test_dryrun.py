from django.test import TestCase
from django.urls import reverse

import json

from ..models import AllDevices


class ConfigureDeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AllDevices.objects.create(
            host="192.168.23.131",
            device_type="cisco_ios",
            device_params="iosxr",
            platform="cisco_xr",
            username="vineeth",
            password="cisco123",
            secret="cisco123",
            hostkey_verify=False,
            allow_agent=False,
            port=22,
        )

    def test_create_netconf(self):

        config_ipv4 = {
            "loopbacks": [
                {"name": 1, "ip_add": "1.1.1.1", "prefix": "255.255.255.255"},
                {"name": 2, "ip_add": "2.2.2.2", "prefix": "255.255.255.255"},
            ],
            "host": "192.168.23.131",
            "dryrun": "True",
            "protocol": "ipv4",
        }
        parsed_json = json.dumps(config_ipv4)

        response = self.client.post(
            reverse("configure"), parsed_json, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_netconf(self):

        config_ipv4 = {
            "loopbacks": [
                {"name": 1, "ip_add": "1.1.1.1", "prefix": "255.255.255.255"},
                {"name": 2, "ip_add": "1.1.1.2", "prefix": "255.255.255.255"},
            ],
            "host": "192.168.23.131",
            "dryrun": "True",
            "protocol": "ipv4",
        }
        parsed_json = json.dumps(config_ipv4)

        response = self.client.delete(
            reverse("configure"), parsed_json, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)