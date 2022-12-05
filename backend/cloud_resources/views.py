from .serializers import DummySerializer, FloatingIPSerializer, NetworkSerializer, RoleSerializer, SecurityGroupSerializer, ServerSerializer, ImageSerializer, FlavorSerializer, RouterSerializer, SubnetSerializer, ProjectSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import generics, status, permissions, serializers
from .connect import conn
import time


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
                disk = str(server.get('flavor', {}).get('disk')) + " GB"
                ram = str(server.get('flavor', {}).get('ram') / 1024)+ " GB"
                vcpus = server.get('flavor', {}).get('vcpus')
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
                "ram": ram,
                "disk": disk,
                "vcpus": vcpus,
                })
            
        return Response(self.serialized_data, status=status.HTTP_200_OK)


    def __init__(self, *args, **kwargs):
        self.allowed_args_dict = {
            "users": (conn.identity.users, UserSerializer, None),
            "projects": (conn.identity.projects, ProjectSerializer, None),
            "roles": (conn.identity.roles, RoleSerializer, None),
            "servers": (conn.compute.servers, ServerSerializer, self.customServerListOutput),
            "networks": (conn.network.networks, NetworkSerializer, None),
            "subnets": (conn.network.subnets, SubnetSerializer, None),
            "images": (conn.image.images, ImageSerializer, None),
            "flavors": (conn.compute.flavors, FlavorSerializer, None),
            "routers": (conn.network.routers, RouterSerializer, None),
            "floating-ip": (conn.list_floating_ips, FloatingIPSerializer, None),
            "security-groups": (conn.list_security_groups, SecurityGroupSerializer, None),
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
            return Response({ "exception": repr(e),
                "detail": repr(e.__dict__)}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({ "exception": repr(e),
                "detail": repr(e.__dict__)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Show a loader till the following line does not returns new server details as API Response.
        return Response(self.serializer.data, status=status.HTTP_201_CREATED)


    
class ResourceDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer
    serialized_data = []

    def __init__(self, *args, **kwargs):
        self.allowed_retrieve_args_dict = {
            "users": (conn.identity.get_user, UserSerializer),
            "projects": (conn.identity.get_project, ProjectSerializer),
            "roles": (conn.identity.get_role, RoleSerializer),
            "servers": (conn.compute.get_server, ServerSerializer),
            "networks": (conn.network.get_network, NetworkSerializer),
            "subnets": (conn.network.get_subnet, SubnetSerializer),
            "images": (conn.image.get_image, ImageSerializer),
            "flavors": (conn.compute.get_flavor, FlavorSerializer),
            "routers": (conn.network.get_router, RouterSerializer),
            "floating-ip": (conn.get_floating_ip, FloatingIPSerializer),
            "security-groups": (conn.get_security_group, SecurityGroupSerializer),
        }

        self.allowed_destroy_args_dict = {
            "users": (conn.identity.delete_user, UserSerializer, None),
            "projects": (conn.identity.delete_project, ProjectSerializer, None),
            # "roles": (conn.identity.delete_role, RoleSerializer, None),
            "servers": (conn.compute.delete_server, ServerSerializer, None),
            "networks": (conn.network.delete_network, NetworkSerializer, self.removeAllResourcesFromNetwork),
            "subnets": (conn.network.delete_subnet, SubnetSerializer, None),
            "images": (conn.image.delete_image, ImageSerializer, None),
            "flavors": (conn.compute.delete_flavor, FlavorSerializer, None),
            "routers": (conn.network.delete_router, RouterSerializer, self.removeAllResourcesFromRouter),
            "floating-ip": (conn.delete_floating_ip, FloatingIPSerializer, None),
            "security-groups": (conn.delete_security_group, SecurityGroupSerializer, None)
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
            return Response({ "exception": repr(e),
                "detail": repr(e.__dict__)}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({ "exception": repr(e),
                "detail": repr(e.__dict__)}, status=status.HTTP_400_BAD_REQUEST)
        
        self.serializer = self.serializer_class(self.queryset)
        return Response(self.serializer.data, status=status.HTTP_200_OK)
    

class ResourceUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DummySerializer
    serialized_data = []
    # queryset_action = None

    def addUserToProject(self, project, request):
        role_id = request.data['role_id']
        user_id = request.data['user_id']
        updated_project = conn.grant_role(role_id, user=user_id, project=project.id, wait=True)
        return updated_project

    def addExternalGatewayToRouter(self, router, request):
        public_network = conn.get_network("public")
        ex_gw_info = conn._build_external_gateway_info(public_network.id, True, None)
        updated_router = conn.network.update_router(router, external_gateway_info=ex_gw_info)
        return updated_router

    def addInternalInterfaceToRouter(self, router, request):
        new_router = conn.network.add_interface_to_router(router, subnet_id=request.data['subnet_id'])
        return new_router

    def startServer(self, server, request):
        conn.compute.start_server(server)
        return conn.compute.wait_for_server(server, status='ACTIVE', failures=None, interval=2, wait=120)

    def stopServer(self, server, request):
        conn.compute.stop_server(server)
        return conn.compute.wait_for_server(server, status='SHUTOFF', failures=None, interval=2, wait=120)

    def associateFloatingIP(self, server, request):
        return conn.add_auto_ip(server, wait=True, timeout=120, reuse=True)

    def addRuleToSecurityGroup(self, security_group, request):
        updated_security_group = conn.create_security_group_rule(security_group.id, 
                                        port_range_min=request.data['port_range_min'], 
                                        port_range_max=request.data['port_range_max'],
                                        protocol=request.data['protocol'],
                                        direction=request.data['direction'])
        return updated_security_group
        

    def deleteRuleFromSecurityGroup(self, security_group, request):
        updated_security_group = conn.delete_security_group_rule(request.data['rule_id'])
        return updated_security_group

    def addSecurityGroup(self, server, request):
        security_group = conn.get_security_group(request.data['security_groups'])
        return conn.compute.add_security_group_to_server(server, security_group)

    def removeSecurityGroup(self, server, request):
        security_group = conn.get_security_group(request.data['security_groups'])
        return conn.compute.remove_security_group_from_server(server, security_group)

    def renameServer(self, server, request):
        return conn.compute.update_server(server, name=request.data['name'])

    def createServerSnapshot(self, server, request):
        return conn.create_image_snapshot(request.data['name'], server, wait=True)

    def resizeServer(self,server, request):
        flavor = conn.compute.get_flavor(request.data['flavor_id'])
        original_flavor_id = server.flavor.id

        if server.flavor.ram > flavor.ram:
            raise serializers.ValidationError({'detail': 'Could not downgrade flavor of the Server.'})
        elif server.flavor.ram == flavor.ram:
            raise serializers.ValidationError({'detail': 'Flavor must be changed to resize the Server.'})
        else:
            try:
                conn.compute.stop_server(server)
                conn.compute.wait_for_server(server, status='SHUTOFF', failures=None, interval=2, wait=120)
            except Exception as e:
                pass

            result = conn.compute.resize_server(server, flavor)
            time.sleep(10)
            
            try:
                result = conn.compute.confirm_server_resize(server)
                time.sleep(20)
            except Exception as e:
                time.sleep(20)
                pass

            conn.compute.start_server(server)
            conn.compute.wait_for_server(server, status='ACTIVE', failures=None, interval=2, wait=120)

            new_server = conn.compute.get_server(server.id)
            
            if original_flavor_id == new_server.flavor.id:
                raise serializers.ValidationError({'detail': 'Error Occurred! Please contact the administrator.'})
            
            return new_server
        


    def __init__(self, *args, **kwargs):
        self.allowed_args_dict = {
            "roles": (conn.identity.get_role, RoleSerializer, {
                # "rename-server": self.renameServer,
            }),
            "users": (conn.identity.get_user, UserSerializer, {
                # "rename-server": self.renameServer,
            }),
            "projects": (conn.identity.get_project, ProjectSerializer, {
                "add-user": self.addUserToProject,
            }),
            "servers": (conn.compute.get_server, ServerSerializer, {
                "start": self.startServer,
                "stop": self.stopServer,
                "allocate-floating-ip": self.associateFloatingIP,
                "add-security-groups": self.addSecurityGroup,
                "remove-security-groups": self.removeSecurityGroup,
                "rename-server": self.renameServer,
                "create-snapshot": self.createServerSnapshot,
                "resize-server": self.resizeServer,
            }),
            "routers": (conn.network.get_router, RouterSerializer, {
                "add-external-gateway": self.addExternalGatewayToRouter,
                "add-internal-interface": self.addInternalInterfaceToRouter,
            }),
            "security-groups": (conn.get_security_group, SecurityGroupSerializer, {
                "add-security-rule": self.addRuleToSecurityGroup,
                "delete-security-rule": self.deleteRuleFromSecurityGroup,
            }),
        }


    def update(self, request, pk, pk2, pk3):
        try:
            self.serialized_data = []
            self.__init__(self)
            # Resource Instance
            self.queryset = self.allowed_args_dict[pk][0](pk2)
            # Resource Serialier
            self.serializer_class = self.allowed_args_dict[pk][1]
            # Resource Action to be updated in the Instance
            self.queryset_action = self.allowed_args_dict[pk][2][pk3](self.queryset, request)

        except KeyError as e:
            return Response({"detail": "Page not found (404)"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({ "exception": repr(e),
                "detail": repr(e.__dict__)}, status=status.HTTP_400_BAD_REQUEST)
        
        self.queryset = self.allowed_args_dict[pk][0](pk2)
        self.serializer = self.serializer_class(self.queryset)
        return Response(self.serializer.data, status=status.HTTP_200_OK)    
