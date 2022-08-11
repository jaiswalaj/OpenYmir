from .serializers import DummySerializer, NetworkSerializer, ServerSerializer, ImageSerializer, FlavorSerializer, RouterSerializer, SubnetSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .connect import conn


class ResourceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer
    serialized_data = []


    def customServerListOutput(self):
        for data in self.serializer.data:
            server = conn.get_server_by_id(data['id'])
            try:
                console_url = conn.compute.get_server_console_url(server=server,console_type="novnc")["url"]
            except:
                console_url = ""

            private_ip = conn.get_server_private_ip(server)
            public_floating_ip = conn.get_server_public_ip(server)

            image_name = ""
            try:
                image_name = conn.image.find_image(server.get('image', {}).get('id'), ignore_missing=False).name
            except:
                image_name = ""
            
            try:
                flavor_name = server.get('flavor', {}).get('name')
            except:
                flavor_name = ""

            self.serialized_data.append({
                "id" : server.get('id'), 
                "name": server.get('name'),
                "status": server.get('status'),
                "console_url": console_url,
                "private_ip": private_ip,
                "public_floating_ip": public_floating_ip,
                "image_name": image_name,
                "flavor": flavor_name,
                })
            
        return Response(self.serialized_data, status=status.HTTP_200_OK)


    def __init__(self, *args, **kwargs):
        self.allowed_args_dict = {
            "servers": (conn.compute.servers, ServerSerializer, self.customServerListOutput),
            "networks": (conn.network.networks, NetworkSerializer, None),
            "subnets": (conn.network.subnets, SubnetSerializer, None),
            "images": (conn.image.images, ImageSerializer, None),
            "flavors": (conn.compute.flavors, FlavorSerializer, None),
            "routers": (conn.network.routers, RouterSerializer, None),
        }


    def list(self, request, pk):
        try:
            self.serialized_data = []
            self.__init__(self)
            self.queryset = self.allowed_args_dict[pk][0]()
            self.serializer_class = self.allowed_args_dict[pk][1]
        except KeyError as e:
            return Response({"detail": "Page not found (404)"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        self.serializer = self.serializer_class(self.queryset, many=True)
        return Response(self.serializer.data, status=status.HTTP_200_OK) if self.allowed_args_dict[pk][2] is None else self.allowed_args_dict[pk][2]()


    def create(self, request, pk):
        try:
            self.serialized_data = []
            self.__init__(self)
            self.queryset = self.allowed_args_dict[pk][0]()
            self.serializer_class = self.allowed_args_dict[pk][1]
            self.serializer = self.serializer_class(data=request.data)
            self.serializer.is_valid(raise_exception=True)
            # Show a loader till the following line does not return a valid JSON Response.
            self.serializer.save()
        except KeyError as e:
            return Response({"detail": "Page not found (404)"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)
        
        # Show a loader till the following line does not returns new server details as API Response.
        return Response(self.serializer.data, status=status.HTTP_201_CREATED)


    
class ResourceDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer
    serialized_data = []

    def __init__(self, *args, **kwargs):
        self.allowed_retrieve_args_dict = {
            "servers": (conn.compute.get_server, ServerSerializer),
            "networks": (conn.network.get_network, NetworkSerializer),
            "subnets": (conn.network.get_subnet, SubnetSerializer),
            "images": (conn.image.get_image, ImageSerializer),
            "flavors": (conn.compute.get_flavor, FlavorSerializer),
            "routers": (conn.network.get_router, RouterSerializer),
        }

        self.allowed_destroy_args_dict = {
            "servers": (conn.compute.delete_server, ServerSerializer, None),
            "networks": (conn.network.delete_network, NetworkSerializer, self.removeAllResourcesFromNetwork),
            "subnets": (conn.network.delete_subnet, SubnetSerializer, None),
            "images": (conn.image.delete_image, ImageSerializer, None),
            "flavors": (conn.compute.delete_flavor, FlavorSerializer, None),
            "routers": (conn.network.delete_router, RouterSerializer, self.removeAllResourcesFromRouter),
        }


    def removeAllFloatingIPsFromRouter(self, router_id):
        floating_ips = conn.list_floating_ips({"router_id": router_id})
        for floating_ip in floating_ips:
            conn.network.delete_ip(floating_ip.id)

 
    def removeAllResourcesFromNetwork(self, network_id):
        ports = conn.list_ports(filters={"network_id": network_id})
        for port in ports:
            server = conn.compute.find_server(port.device_id)
            if server is None:
                continue
            else:
                conn.compute.delete_server(port.device_id)
                conn.compute.wait_for_delete(server)
        
        ports = conn.list_ports(filters={"network_id": network_id})
        for port in ports:
            try:
                router = conn.network.get_router(port.device_id)
                updated_router = conn.network.remove_interface_from_router(router, subnet_id=port.fixed_ips[0]['subnet_id'])
            except:
                pass    


    def removeAllResourcesFromRouter(self, router_id):
        self.removeAllFloatingIPsFromRouter(router_id)
        subnet_id_list = conn.network.subnets()
        for subnet_id in subnet_id_list:
            try:
                conn.network.remove_interface_from_router(router_id, subnet_id.id)
            except Exception as e:
                pass


    def destroy(self,request, pk, pk2):
        try:
            self.serialized_data = []
            self.__init__(self)

            if self.allowed_destroy_args_dict[pk][2] is not None:
                self.allowed_destroy_args_dict[pk][2](pk2) 
            
            self.queryset = self.allowed_destroy_args_dict[pk][0](pk2)
            self.serializer_class = self.allowed_destroy_args_dict[pk][1]
        except KeyError as e:
            return Response({"detail": "Page not found (404)"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "The resource is being deleted"}, status=status.HTTP_204_NO_CONTENT)        


    def retrieve(self, request, pk, pk2):
        try:
            self.serialized_data = []
            self.__init__(self)
            self.queryset = self.allowed_retrieve_args_dict[pk][0](pk2)
            self.serializer_class = self.allowed_retrieve_args_dict[pk][1]
        except KeyError as e:
            return Response({"detail": "Page not found (404)"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)
        
        self.serializer = self.serializer_class(self.queryset)
        return Response(self.serializer.data, status=status.HTTP_200_OK)
    

class ResourceUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer

    def update(self, request, pk, pk2, pk3):
        try:
            if pk == "servers":
                server = conn.compute.get_server(pk2)
                if pk3 == "start":
                    self.resource = conn.compute.start_server(pk2)
                    self.serializer_class = ServerSerializer
                    # Show a loader till the following line does not return a Server object.
                    conn.compute.wait_for_server(server, status='ACTIVE', failures=None, interval=2, wait=120)
                    # Show a loader till the following line does not return the given message as API Response.
                    self.messgae = {"detail": "Server Started"}
                elif pk3 == "stop":
                    self.resource = conn.compute.stop_server(pk2)
                    self.serializer_class = ServerSerializer
                    # Show a loader till the following line does not return a Server object.
                    conn.compute.wait_for_server(server, status='ACTIVE', failures=None, interval=2, wait=120)
                    # Show a loader till the following line does not return the given message as API Response.
                    self.messgae = {"detail": "Server Stopped"}
                elif pk3 == "allocate-floating-ip":
                    self.serializer_class = ServerSerializer
                    self.resource = conn.add_auto_ip(server, wait=True, timeout=60, reuse=True)
                    self.messgae = {"detail": "For Server ID: "+pk2+", Floating IP Allocated is: "+self.resource}
                else:
                    self.resource = None
                    self.serializer_class = DummySerializer
            else:
                self.resource = None
                self.serializer_class = DummySerializer
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        if self.serializer_class == DummySerializer:
            return Response({"detail": "URL Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.messgae, status=status.HTTP_200_OK)
