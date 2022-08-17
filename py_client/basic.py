from threading import Timer
import requests
# from requests.auth import HTTPBasicAuth
from resources_var_test import resources as user_script
from resources_var_test import username, password
from endpoints import *

image_dict = {}
flavor_dict = {}
network_dict = {}
subnet_dict = {}
router_dict = {}
server_dict = {}
floating_ip_dict = {}
user_auth_details = requests.auth.HTTPBasicAuth(username, password)


def create_network(data_list):
    network_name = data_list[0]
    subnet_cidr = data_list[1]

    network = requests.post(parent_endpoint+network_list_endpoint, auth = user_auth_details, data = {"name": network_name})
    network_id = network.json()['id']
    temp = {network_id: network_name}
    network_dict.update(temp)
    print("New Network created with ID: "+network_id+" and Name: "+network_name)

    subnet_name = network_name+"_subnet"

    subnet = requests.post(parent_endpoint+subnet_list_endpoint, auth = user_auth_details, data = {
        "name": subnet_name, 
        "network_id": network_id,
        "cidr": subnet_cidr,
    })
    subnet_id = subnet.json()['id']
    temp = {subnet_id: subnet_name}
    subnet_dict.update(temp)
    print("New Subnet created with ID: "+subnet_id+" and Name: "+subnet_name)


def create_router(data_list):
    router_name = data_list[0]
    external_gateway_bool = data_list[1]
    internal_interface_list = data_list[2]

    router = requests.post(parent_endpoint+router_list_endpoint, auth = user_auth_details, data = {"name": router_name})
    router_id = router.json()['id']
    temp = {router_id: router_name}
    router_dict.update(temp)
    print("New Router Created with ID: "+router_id+" Name: "+router_name)
    
    if external_gateway_bool is True:
        updated_router = requests.put(parent_endpoint+router_list_endpoint+router_id+"/"+router_add_external_gateway_endpoint, auth = user_auth_details)
        print("Router connected to External Gateway.")

    for internal_interface in internal_interface_list:
        subnet_name = internal_interface+"_subnet"
        subnet_id = list(subnet_dict.keys())[list(subnet_dict.values()).index(subnet_name)]
        updated_router = requests.put(parent_endpoint+router_list_endpoint+router_id+"/"+router_add_internal_interface_endpoint, auth = user_auth_details, data = {"subnet_id": subnet_id})
        print("Router connected to Internal Interface :- \nSubnet ID: "+subnet_id+" Subnet Name: "+subnet_name)

    
def create_server(data_list):
    server_name = data_list[0]
    image_name = data_list[1]
    flavor_name = data_list[2]
    network_name = data_list[3]
    floating_ip_bool = data_list[4]
    server_status = data_list[5]

    image_id = list(image_dict.keys())[list(image_dict.values()).index(image_name)]
    flavor_id = list(flavor_dict.keys())[list(flavor_dict.values()).index(flavor_name)]
    network_id = list(network_dict.keys())[list(network_dict.values()).index(network_name)]
    
    server = requests.post(parent_endpoint+server_list_endpoint, auth = user_auth_details, data = {"name": server_name, "image_id": image_id, "flavor_id": flavor_id, "networks": network_id})
    server_id = server.json()['id']
    temp = {server_id: server_name}
    server_dict.update(temp)
    print("New Server created with ID: "+server_id+" Name: "+server_name)
    
    if floating_ip_bool is True:
        updated_server = requests.put(parent_endpoint+server_list_endpoint+server_id+"/"+server_allocate_floating_ip_endpoint, auth = user_auth_details)
        for data in updated_server.json()['addresses'][network_name]:
            if data['OS-EXT-IPS:type'] == "floating":
                public_floating_ip = data['addr']
        temp = {server_id: public_floating_ip}
        floating_ip_dict.update(temp)
        print("Server associated with Floating IP: "+public_floating_ip)
        
    if server_status.upper() == "SHUTOFF":
        updated_server = requests.put(parent_endpoint+server_list_endpoint+server_id+"/"+server_stop_endpoint, auth = user_auth_details)
        print("Server status updated to SHUTOFF")
    

allowed_resource_args = {
    "network": create_network,
    "router": create_router,
    "server": create_server,
}

def big_crunch():
    network_id_list = list(network_dict.keys())
    for id in network_id_list:
        print("Network ID: "+id+" Name: "+network_dict[id])
        response_received = requests.delete(parent_endpoint+network_list_endpoint+id, auth = user_auth_details)
        print(response_received)

    router_id_list = list(router_dict.keys())
    for id in router_id_list:
        print("Router ID: "+id+" Name: "+router_dict[id])
        response_received = requests.delete(parent_endpoint+router_list_endpoint+id, auth = user_auth_details)
        print(response_received)

    floating_ip_id_list = list(floating_ip_dict.keys())
    for id in floating_ip_id_list:
        print("Floating ID: "+id+" Name: "+floating_ip_dict[id])
        response_received = requests.delete(parent_endpoint+floating_ip_list_endpoint+id, auth = user_auth_details)
        print(response_received)

def big_bang():
    response_received = requests.get(parent_endpoint+image_list_endpoint, auth = user_auth_details)
    for image in response_received.json():
        temp = {image['id']: image['name']}
        image_dict.update(temp)

    response_received = requests.get(parent_endpoint+flavor_list_endpoint, auth = user_auth_details)
    for flavor in response_received.json():
        temp = {flavor['id']: flavor['name']}
        flavor_dict.update(temp)

    for resource in user_script:
        for data in resource['details']:
            data_value_list = list(data.values())
            allowed_resource_args[resource['resource']](data_value_list)
            
    print("All Resources Generated Successfully")
    time_interval = Timer(15, big_crunch)
    time_interval.start()

big_bang()