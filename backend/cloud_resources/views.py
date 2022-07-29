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
        self.__init__(self, pk=pk)
        if self.serializer_class == DummySerializer:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.serializer = self.serializer_class(self.queryset, many=True)
        return Response(self.serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk):
        self.__init__(self, pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
