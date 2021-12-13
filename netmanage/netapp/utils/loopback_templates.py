LOOPBACK_IPV4_CONFIG = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
{% for loopback in loopbacks %}
    <interface-configuration xc:operation="create">
    <active>act</active>
    <interface-name>Loopback{{ loopback.name }}</interface-name>
    <interface-virtual></interface-virtual>
    <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
     <addresses>
      <primary>
       <address>{{ loopback.ip_add }}</address>
       <netmask>{{ loopback.prefix}}</netmask>
      </primary>
     </addresses>
    </ipv4-network>
   </interface-configuration>
   {% endfor %}
</interface-configurations>
</config>
"""

LOOPBACK_IPV6_CONFIG = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
{% for loopback in loopbacks %}
 <interface-configuration xc:operation="create">
  <active>act</active>
  <interface-name>Loopback{{ loopback.name }}</interface-name>
  <interface-virtual></interface-virtual>
  <ipv6-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv6-ma-cfg">
   <addresses>
    <regular-addresses>
     <regular-address>
      <address>{{ loopback.ip_add }}</address>
      <prefix-length>{{ loopback.prefix }}</prefix-length>
     </regular-address>
    </regular-addresses>
   </addresses>
  </ipv6-network>
 </interface-configuration>
{% endfor %}
</interface-configurations>
</config>
"""

LOOPBACK_DELETE_CONFIG = """
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
