import requests
from requests.auth import HTTPBasicAuth
from resources_var_test import resources

endpoint = "http://127.0.0.1:8000/api/resources/"
img_endpoint = "images/"
flv_endpoint = "flavors/"
net_endpoint = "networks/"
sub_endpoint = "subnets/"
rou_endpoint = "routers/"
ser_endpoint = "servers/"

get_response = requests.get(endpoint+img_endpoint, auth = HTTPBasicAuth('admin', 'admin'))
image_dict = {}
for data in get_response.json():
    temp = {data['id']: data['name']}
    image_dict.update(temp)


get_response = requests.get(endpoint+flv_endpoint, auth = HTTPBasicAuth('admin', 'admin'))
flavor_dict = {}
for data in get_response.json():
    temp = {data['id']: data['name']}
    flavor_dict.update(temp)


for resource in resources:
    net_name = resource['name']
    network = requests.post(endpoint+net_endpoint, auth = HTTPBasicAuth('admin', 'admin'), data = {"name": net_name})
    net_id = network.json()['id']
    print("New Network Created with ID: "+net_id+" Name: "+net_name)
    
    subnet_name = resource['name']+"_subnet"
    subnet = requests.post(endpoint+sub_endpoint, auth = HTTPBasicAuth('admin', 'admin'), data = {
        "name": subnet_name, 
        "network_id": net_id,
        "cidr": resource['subnet_cidr'],
        })
    subnet_id = subnet.json()['id']
    print("New Subnet Created with ID: "+subnet_id+" Name: "+subnet_name)

    router_name = resource['name']+"_"+resource['router_name']
    router = requests.post(endpoint+rou_endpoint, auth = HTTPBasicAuth('admin', 'admin'), data = {"name": router_name})
    router_id = router.json()['id']
    updated_router = requests.put(endpoint+rou_endpoint+router_id+"/add-external-gateway/", auth = HTTPBasicAuth('admin', 'admin'))
    updated_router = requests.put(endpoint+rou_endpoint+router_id+"/add-internal-interface/", auth = HTTPBasicAuth('admin', 'admin'), data = {"subnet_id": subnet_id})
    print("New Router Created with ID: "+router_id+" Name: "+router_name)

    for server in resource['server_details']:
        img_id = list(image_dict.keys())[list(image_dict.values()).index(server['image_name'])]
        flv_id = list(flavor_dict.keys())[list(flavor_dict.values()).index(server['flavor_name'])]
        server_name = resource['name']+"_"+server['server_name']
        
        new_server = requests.post(endpoint+ser_endpoint, auth = HTTPBasicAuth('admin', 'admin'), data = {"name": server_name, "image_id": img_id, "flavor_id": flv_id, "networks": net_id})
        new_server_id = new_server.json()['id']
        
        if server['floating_ip'] is True:
            new_server = requests.put(endpoint+ser_endpoint+new_server_id+"/allocate-floating-ip/", auth = HTTPBasicAuth('admin', 'admin'))
            
        if server['status'].upper() == "SHUTOFF":
            new_server = requests.put(endpoint+ser_endpoint+new_server_id+"/stop/", auth = HTTPBasicAuth('admin', 'admin'))
        
        print("New Server Created with ID: "+new_server_id+" Name: "+server_name)
        

# Sends HTTP Request to the endpoint URL and returns the Response




# get_response = requests.

# Prints the response as text which is an HTML source code
# print(get_response.text)
# print(get_response.status_code)



