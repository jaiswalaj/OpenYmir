from .serializers import DummySerializer, NetworkSerializer, ServerSerializer, ImageSerializer, FlavorSerializer, RouterSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions
import openstack

openstack.enable_logging(debug=True)
conn=openstack.connection.Connection(auth_url='http://192.168.56.101/identity/v3',
                           project_name='admin',username='admin',
                           password='nomoresecret',
                           user_domain_id='default',
                           project_domain_id='default', verify=False)



class ResourceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer
    serialized_data = []

    def __init__(self, *args, **kwargs):
        if kwargs.get("pk") == "servers":
            self.queryset = conn.compute.servers()
            self.serializer_class = ServerSerializer
        elif kwargs.get("pk") == "networks":
            self.queryset = conn.network.networks()
            self.serializer_class = NetworkSerializer
        elif kwargs.get("pk") == "images":
            self.queryset = conn.image.images()
            self.serializer_class = ImageSerializer
        elif kwargs.get("pk") == "flavors":
            self.queryset = conn.compute.flavors()
            self.serializer_class = FlavorSerializer
        elif kwargs.get("pk") == "routers":
            self.queryset = conn.network.routers()
            self.serializer_class = RouterSerializer
        else:
            self.queryset = None
            self.serializer_class = DummySerializer
    
    def list(self, request, pk):
        try:
            self.serialized_data = []
            self.__init__(self, pk=pk)
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        if self.serializer_class == DummySerializer:
            return Response({"detail": "URL Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        self.serializer = self.serializer_class(self.queryset, many=True)

        if pk == "servers":
            for data in self.serializer.data:
                console_url = conn.compute.get_server_console_url(server=data['id'],console_type="novnc")["url"]
                
                address_list = []
                for key in data['addresses']:
                    for address_data in data['addresses'][key]:
                        address_list.append(address_data['addr'])

                image_name = ""
                imageID = data['image'].split("id=")[1].split(",")[0]
                imageDetails = conn.image.find_image(imageID, ignore_missing=False)
                image_name = imageDetails.name

                flavor_name = data['flavor'].split("original_name=")[1].split(",")[0]
                
                self.serialized_data.append({
                    "id" : data['id'], 
                    "name": data['name'],
                    "status": data['status'],
                    "console_url": console_url,
                    "addresses": address_list,
                    "image_name": image_name,
                    "flavor": flavor_name,
                    })

            return Response(self.serialized_data, status=status.HTTP_200_OK)


        return Response(self.serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk):
        try:
            self.__init__(self, pk=pk)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Show a loader till the following line does not return a Server object.
            serializer.save()
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)
        
        # Show a loader till the following line does not returns new server details as API Response.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
class ResourceDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer

    def retrieve(self, request, pk, pk2):
        try:
            if pk == "servers":
                self.resource = conn.compute.get_server(pk2)
                self.serializer_class = ServerSerializer
            elif pk == "networks":
                self.resource = conn.network.get_network(pk2)
                self.serializer_class = NetworkSerializer
            elif pk == "images":
                self.resource = conn.image.get_image(pk2)
                self.serializer_class = ImageSerializer
            elif pk == "flavors":
                self.resource = conn.compute.get_flavor(pk2)
                self.serializer_class = FlavorSerializer
            elif pk == "routers":
                self.resource = conn.network.get_router(pk2)
                self.serializer_class = RouterSerializer
            else:
                self.resource = None
                self.serializer_class = DummySerializer
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        if self.serializer_class == DummySerializer:
            return Response({"detail": "URL Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(self.resource)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self,request, pk, pk2):
        try:
            if pk == "servers":
                self.resource = conn.compute.delete_server(pk2)
                self.serializer_class = ServerSerializer
            elif pk == "networks":
                self.resource = conn.network.delete_network(pk2)
                self.serializer_class = NetworkSerializer
            elif pk == "images":
                self.resource = conn.image.delete_image(pk2)
                self.serializer_class = ImageSerializer
            elif pk == "flavors":
                self.resource = conn.compute.delete_flavor(pk2)
                self.serializer_class = FlavorSerializer
            elif pk == "routers":
                self.resource = conn.network.delete_router(pk2)
                self.serializer_class = RouterSerializer
            else:
                self.resource = None
                self.serializer_class = DummySerializer
        except Exception as e:
            return Response({"detail": repr(e)}, status=status.HTTP_404_NOT_FOUND)

        if self.serializer_class == DummySerializer or self.resource is None:
            return Response({"detail": "URL Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "The Resource is being Deleted"}, status=status.HTTP_204_NO_CONTENT)
    


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
