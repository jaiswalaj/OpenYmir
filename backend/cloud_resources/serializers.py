from django.http import Http404
from rest_framework import serializers
from .connect import conn

class DummySerializer(serializers.Serializer):
    messgae = serializers.CharField(max_length=1, read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class ServerSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    links = serializers.ListField(read_only=True)
    addresses = serializers.DictField(read_only=True)
    attached_volumes = serializers.CharField(read_only=True)
    interface_ip = serializers.CharField(read_only=True)
    key_name = serializers.CharField(read_only=True)
    server_groups = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    image = serializers.CharField(read_only=True)
    image_id = serializers.CharField(max_length=100, required=True)
    flavor = serializers.CharField(read_only=True)
    flavor_id = serializers.CharField(max_length=50, required=True)
    status = serializers.CharField(read_only=True)
    power_state = serializers.CharField(read_only=True)
    networks = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        serverCreated = conn.compute.create_server(name=validated_data["name"], image_id=validated_data["image_id"], 
                flavor_id=validated_data["flavor_id"], networks=[{"uuid": validated_data["networks"]}])
        serverWait = conn.compute.wait_for_server(serverCreated)
        return serverWait


class NetworkSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    status = serializers.CharField(read_only=True)
    is_default = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        new_network = conn.network.create_network(name=validated_data['name'])
        return new_network



class SubnetSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    status = serializers.CharField(read_only=True)
    network_id = serializers.CharField(max_length=100, required=True)
    ip_version = serializers.IntegerField(read_only=True)
    cidr = serializers.CharField(max_length=20, required=True)

    def create(self, validated_data):
        cidr = validated_data['cidr']
        new_subnet = conn.network.create_subnet(name=validated_data["name"], network_id=validated_data["network_id"], ip_version=4, cidr=cidr)
        return new_subnet


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class FlavorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class RouterSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    status = serializers.CharField(read_only=True)
    external_gateway_info = serializers.DictField(read_only=True)
    subnet_id = serializers.CharField(max_length=100, required=False)


    def create(self, validated_data):
        new_router = conn.network.create_router(name=validated_data["name"])
        return new_router
        

class FloatingIPSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    fixed_ip_address = serializers.IPAddressField(read_only=True)
    floating_ip_address = serializers.IPAddressField(read_only=True)
    router_id = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Page not found (404)")


class SecurityGroupSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=50, required=True)
    description = serializers.CharField(max_length=100, required=True)
    stateful = serializers.BooleanField(read_only=True)
    security_group_rules = serializers.ListField(read_only=True)
    rule_id = serializers.CharField(max_length=50, required=False)
    port_range_min = serializers.IntegerField(required=False)
    port_range_max = serializers.IntegerField(required=False)
    protocol = serializers.CharField(max_length=20, required=False)     
    # Allowed Protocol Inputs: [None, 'ah', 'dccp', 'egp', 'esp', 'gre', 'hopopt', 'icmp', 'igmp', 'ip', 'ipip', 'ipv6-encap', 'ipv6-frag', 'ipv6-icmp', 'icmpv6', 'ipv6-nonxt', 'ipv6-opts', 'ipv6-route', 'ospf', 'pgm', 'rsvp', 'sctp', 'tcp', 'udp', 'udplite', 'vrrp'] and integer representations [0 to 255] are supported.
    direction = serializers.CharField(max_length=10, required=False)    # ingress and egress

    def create(self, validated_data):
        new_security_group = conn.create_security_group(validated_data["name"], validated_data["description"])
        return new_security_group


# class SecurityGroupRuleSerializer(serializers.Serializer):
#     id = serializers.CharField(read_only=True)
#     name = serializers.CharField(max_length=50, required=True)
#     description = serializers.CharField(max_length=100, required=True)
#     stateful = serializers.BooleanField(read_only=True)
#     security_group_rules = serializers.ListField(read_only=True)

#     def create(self, validated_data):
#         new_security_group = conn.create_security_group(validated_data["name"], validated_data["description"])
#         return new_security_group
