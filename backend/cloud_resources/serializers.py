from django.http import Http404
from rest_framework import serializers
from .connect import conn
import base64

class DummySerializer(serializers.Serializer):
    messgae = serializers.CharField(max_length=1, read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class ServerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    image = serializers.CharField(read_only=True)
    image_id = serializers.CharField(max_length=100, required=True)
    flavor = serializers.CharField(read_only=True)
    flavor_id = serializers.CharField(max_length=50, required=True)
    networks = serializers.CharField(max_length=100, required=True)
    
    launched_at = serializers.DateTimeField(read_only=True)
    terminated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(max_length=50, required=False)
    server_groups = serializers.CharField(read_only=True)
    security_groups = serializers.CharField(max_length=300, required=False)
    power_state = serializers.CharField(read_only=True)
    attached_volumes = serializers.CharField(read_only=True)
    key_name = serializers.CharField(read_only=True)
    interface_ip = serializers.CharField(read_only=True)
    addresses = serializers.DictField(read_only=True)
    links = serializers.ListField(read_only=True)
    
    def create(self, validated_data):
        # Here we are setting default password as "openstack" for all servers being created if user does not provide any password.
        if "password" in validated_data.keys():
            plain_password = validated_data["password"]
        else:
            plain_password = "openstack"

        # Customization script for configuring the password and other related settings for the server.
        plain_customization_script = """#cloud-config
password: """+plain_password+"""
chpasswd: { expire: False }
ssh_pwauth: True"""

        # The customization script can only be sent as "user_data" only in base64 encoded format.
        ascii_customization_script = plain_customization_script.encode("ascii")
        encoded_customization_script = base64.b64encode(ascii_customization_script)

        # Converting base64 encoded object into string to pass it as "user_data" for creating server with customized settings.
        user_data = str(encoded_customization_script, 'UTF-8')

        # Creating Server with the input provided by the user.
        serverCreated = conn.compute.create_server(name=validated_data["name"], image_id=validated_data["image_id"], 
                flavor_id=validated_data["flavor_id"], networks=[{"uuid": validated_data["networks"]}], user_data=user_data)

        # Waiting for the server to be created successfully.
        serverWait = conn.compute.wait_for_server(serverCreated)

        return serverWait


class NetworkSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    is_default = serializers.BooleanField(read_only=True)
    is_router_external = serializers.BooleanField(read_only=True)
    provider_network_type = serializers.CharField(read_only=True)
    provider_physical_network = serializers.CharField(read_only=True)

    subnets = serializers.CharField(read_only=True)

    def create(self, validated_data):
        new_network = conn.network.create_network(name=validated_data['name'])
        return new_network



class SubnetSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    ip_version = serializers.IntegerField(read_only=True)
    network_id = serializers.CharField(max_length=100, required=True)
    cidr = serializers.CharField(max_length=20, required=True)
    gateway_ip = serializers.CharField(read_only=True)
    allocation_pools = serializers.CharField(read_only=True)
    dns_nameservers = serializers.CharField(read_only=True)
    host_routes = serializers.CharField(read_only=True)
    is_dhcp_enabled = serializers.BooleanField(read_only=True)

    service_types = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        cidr = validated_data['cidr']
        new_subnet = conn.network.create_subnet(name=validated_data["name"], network_id=validated_data["network_id"], ip_version=4, cidr=cidr)
        return new_subnet


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    container_format = serializers.CharField(read_only=True)
    disk_format = serializers.CharField(read_only=True)
    size = serializers.CharField(read_only=True)
    virtual_size = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class FlavorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    
    disk = serializers.CharField(read_only=True)        # Disk Size in GB
    ram = serializers.CharField(read_only=True)         # Ram Size in MB
    vcpus = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class RouterSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    is_distributed = serializers.BooleanField(read_only=True)
    is_ha = serializers.BooleanField(read_only=True)
    routes = serializers.CharField(read_only=True)

    external_gateway_info = serializers.DictField(read_only=True)
    subnet_id = serializers.CharField(max_length=100, required=False)
    

    def create(self, validated_data):
        new_router = conn.network.create_router(name=validated_data["name"])
        return new_router
        

class FloatingIPSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    attached = serializers.BooleanField(read_only=True)
    fixed_ip_address = serializers.IPAddressField(read_only=True)
    floating_ip_address = serializers.IPAddressField(read_only=True)
    properties = serializers.CharField(read_only=True)

    port = serializers.CharField(read_only=True)
    router_id = serializers.CharField(read_only=True)
    network = serializers.CharField(read_only=True)
    floating_network_id = serializers.CharField(read_only=True)


    def create(self, validated_data):
        raise Http404("Page not found (404)")


class SecurityGroupSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(max_length=100, required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    stateful = serializers.BooleanField(read_only=True)
    security_group_rules = serializers.ListField(read_only=True)

    rule_id = serializers.CharField(max_length=50, required=False)
    protocol = serializers.CharField(max_length=20, required=False)     
    direction = serializers.CharField(max_length=10, required=False)    # ingress and egress
    port_range_min = serializers.IntegerField(required=False)
    port_range_max = serializers.IntegerField(required=False)
    # Allowed Protocol Inputs: [None, 'ah', 'dccp', 'egp', 'esp', 'gre', 'hopopt', 'icmp', 'igmp', 'ip', 'ipip', 'ipv6-encap', 'ipv6-frag', 'ipv6-icmp', 'icmpv6', 'ipv6-nonxt', 'ipv6-opts', 'ipv6-route', 'ospf', 'pgm', 'rsvp', 'sctp', 'tcp', 'udp', 'udplite', 'vrrp'] and integer representations [0 to 255] are supported.

    def create(self, validated_data):
        new_security_group = conn.create_security_group(validated_data["name"], validated_data["description"])
        return new_security_group


class ProjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    
    is_domain = serializers.BooleanField(read_only=True)
    is_enabled = serializers.BooleanField(read_only=True)
    domain_id = serializers.CharField(read_only=True)
    parent_id = serializers.CharField(read_only=True)
    options = serializers.CharField(read_only=True)

    user_id = serializers.CharField(max_length=100, write_only=True, required=False)
    role_id = serializers.CharField(max_length=100, write_only=True, required=False)
    
    def create(self, validated_data):
        new_project = conn.identity.create_project(name=validated_data['name'])
        return new_project


class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.CharField(max_length=100)
    description = serializers.CharField(read_only=True)
    
    is_enabled = serializers.BooleanField(read_only=True)
    domain_id = serializers.CharField(read_only=True)
    default_project_id = serializers.CharField(read_only=True)

    password = serializers.CharField(max_length=100, required=True, write_only=True)
    password_expires_at = serializers.CharField(read_only=True)

    def create(self, validated_data):
        new_user = conn.identity.create_user(name=validated_data['name'], email=validated_data['email'], password=validated_data['password'])
        return new_user


class RoleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(read_only=True)
    
    domain_id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")