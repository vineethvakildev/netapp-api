loopback_config = """
<config>
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
{% for loopback in loopbacks %}
    <interface-configuration>
    <active>act</active>
    <interface-name>Loopback{{ loopback.name }}</interface-name>
    <interface-virtual></interface-virtual>
    <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
     <addresses>
      <primary>
       <address>{{ loopback.ipv4_add }}</address>
       <netmask>255.255.255.255</netmask>
      </primary>
     </addresses>
    </ipv4-network>
   </interface-configuration>
   {% endfor %}
</interface-configurations>
</config>
"""

loopback_delete_config = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    {% for loopback in loopbacks %}
    <interface-configuration xc:operation="delete">
    <active>act</active>
    <interface-name>Loopback{{ loopback.name }}</interface-name>
   </interface-configuration>
   {% endfor %}
</interface-configurations>
</config>
"""
