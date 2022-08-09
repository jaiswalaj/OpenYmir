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
    name = serializers.CharField(max_length=100)
    image = serializers.CharField(read_only=True)
    image_id = serializers.CharField(max_length=500)
    flavor = serializers.CharField(read_only=True)
    flavor_id = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=20, read_only=True)
    power_state = serializers.CharField(max_length=20, read_only=True)
    networks = serializers.CharField(max_length=500)

    def create(self, validated_data):
        serverCreated = conn.compute.create_server(name=validated_data["name"], image_id=validated_data["image_id"], 
                flavor_id=validated_data["flavor_id"], networks=[{"uuid": validated_data["networks"]}])
        serverWait = conn.compute.wait_for_server(serverCreated)

        return serverWait


class NetworkSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    is_default = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")

class ImageSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")


class FlavorSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")


class RouterSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100, read_only=True)
    status = serializers.CharField(max_length=20, read_only=True)
    external_gateway_info = serializers.DictField(read_only=True)

    def create(self, validated_data):
        raise Http404("Forbidden Request")
