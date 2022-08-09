from django.http import Http404
from django.urls import Resolver404
from rest_framework import serializers
from .connect import conn

class DummySerializer(serializers.Serializer):
    messgae = serializers.CharField(max_length=10, read_only=True)

    def create(self, validated_data):
        raise Resolver404()


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
        # raise Http404("Forbidden Request")
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
        cidr = "10.0.0.0/"+validated_data['cidr']
        new_subnet = conn.network.create_subnet(name=validated_data["name"], network_id=validated_data["network_id"], ip_version=4, cidr=cidr)
        return new_subnet


class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")


class FlavorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")


class RouterSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    status = serializers.CharField(read_only=True)
    external_gateway_info = serializers.DictField(read_only=True)

    def create(self, validated_data):
        new_router = conn.network.create_router(name=validated_data["name"])
        return new_router
        # raise Http404("Forbidden Request")
