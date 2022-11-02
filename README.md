# OpenYmir
## Django Rest API based on OpenStack SDK



OpenYmir is built using Django Rest Framework and OpenStack SDK to provide  features through which one can perform various operations on OpenStack (an open standard cloud computing platform, mostly deployed as infrastructure-as-a-service). 

OpenYmir allows you to perform CRUD operations on Networks, Subnets, Routers, Servers, Security Groups, and Floating IPs. Some key highlights of the operations which can be performed using OpenYmir API calls are as follows:-

- Create, List, Retrieve, and Delete Projects, and Users
- Assign Users to Projects with specific Roles
- Create, List, Retrieve, Delete, Rename, Start and Stop a Server
- Allocate Floating IP to a Server
- Delete a Network completely and safely ( i.e. deleting Servers on the Network but not Routers)
- Provide proper Exceptions in case of any failure


## API Endpoints
Following are the enpoints and the type of request which needs to make to perform various operations on OpenStack Cloud Platform. However, for the sake of ease Domain Name is being replaced by "127.0.0.1:8000" in the endpoints listed below.

List Resources (GET Request)
- http://127.0.0.1:8000/api/resources/users/
- http://127.0.0.1:8000/api/resources/projects/
- http://127.0.0.1:8000/api/resources/roles/
- http://127.0.0.1:8000/api/resources/servers/
- http://127.0.0.1:8000/api/resources/networks/
- http://127.0.0.1:8000/api/resources/subnets/
- http://127.0.0.1:8000/api/resources/images/
- http://127.0.0.1:8000/api/resources/flavors/
- http://127.0.0.1:8000/api/resources/routers/
- http://127.0.0.1:8000/api/resources/floating-ip/
- http://127.0.0.1:8000/api/resources/security-groups/

Create Resources (POST Request)
- Data Required for creating User: Name, Email, and Password
-- http://127.0.0.1:8000/api/resources/users/
- Data Required for creating Project: Name
-- http://127.0.0.1:8000/api/resources/projects/
- Data Required for creating Server: Name, Image ID, Flavor ID, Network ID, and Password(optional)
-- http://127.0.0.1:8000/api/resources/servers/
- Data Required for creating Network: Name
-- http://127.0.0.1:8000/api/resources/networks/
- Data Required for creating Subnet: Name, Network ID, and CIDR
-- http://127.0.0.1:8000/api/resources/subnets/
- Data Required for creating Router: Name
-- http://127.0.0.1:8000/api/resources/subnets/
- Data Required for creating Security Group: Name, and Description
-- http://127.0.0.1:8000/api/resources/security-groups/

<br/>

>Note: Default password for the servers being created without providing custom password will be `openstack`.

<br/>

Retrieve Details (GET Request) and Destroy (DELETE Request) a Resource
- http://127.0.0.1:8000/api/resources/users/"User ID Here"/
- http://127.0.0.1:8000/api/resources/projects/"Project ID Here"/
- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/
- http://127.0.0.1:8000/api/resources/networks/"Network ID Here"/
- http://127.0.0.1:8000/api/resources/subnets/"Subnet ID Here"/
- http://127.0.0.1:8000/api/resources/images/"Image ID Here"/
- http://127.0.0.1:8000/api/resources/flavors/"Flavor ID Here"/
- http://127.0.0.1:8000/api/resources/routers/"Router ID Here"/
- http://127.0.0.1:8000/api/resources/floating-ip/"Floating IP ID Here"/
- http://127.0.0.1:8000/api/resources/security-groups/"Security Group ID Here"/

Update (PUT Request) a Resource

- Data Required to add a User to a Project with a specific Role: User ID/Name and Role ID/Name
-- http://127.0.0.1:8000/api/resources/projects/"Project ID Here"/add-user


- Data Required to start a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/start
- Data Required to stop a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/stop
- Data Required to allocate a Floating IP to a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/allocate-floating-ip
- Data Required to rename a Server: Name
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/rename-server
- Data Required to add a Security Group to a Server: Security Group ID
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/add-security-groups
- Data Required to remove a Security Group from a Server: Security Group ID
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/remove-security-groups


- Data Required to add External Gateway to a Router: None (Limitation: External Gateway Network must be named as "public")
-- http://127.0.0.1:8000/api/resources/routers/"Router ID Here"/add-external-gateway
- Data Required to add Internal Interface to a Router: Subnet ID
-- http://127.0.0.1:8000/api/resources/routers/"Router ID Here"/add-internal-interface


- Data Required to add new Security Rule to a Security Group: Port range min(initial port number of the range), Port range max(final port number of the range), Protocol, and Direction
-- http://127.0.0.1:8000/api/resources/security-groups/"Security Group ID Here"/add-security-rule
- Data Required to delete a Security Rule from a Security Group: Security Rule ID
-- http://127.0.0.1:8000/api/resources/security-groups/"Security Group ID Here"/delete-security-rule

## JSON Properties
JSON properties that should be used to pass values into the endpoints via curl requests.

| Name | Property |
| ---- | -------- |
| Name | { "name": "Name of the Resource here" } |
| Email | { "email": "Email of the User here" } |
| Password | { "password": "Custom Password for the resource being created here" } |
| Image ID | { "image_id": "ID of a pre-existing Image here" } |
| Flavor ID | { "flavor_id": "ID of a pre-existing Flavor here" } |
| Network ID | { "networks": "ID of a pre-existing Network here" } |
| User ID | { "user_id": "ID of a pre-existing User here" } |
| Role ID | { "role_id": "ID of a pre-existing Role here" } |
| CIDR | { "cidr": "CIDR of the Subnet to be created here" } |
| Description  | { "description": "Description of the Security Group here" } |
| Security Group ID | { "security_groups": "ID of a pre-existing Security Group here" } |
| Subnet ID | { "subnet_id": "ID of a pre-existing Subnet here" } |
| Port range min | { "port_range_min": "Port Range starting point here" } |
| Port range max | { "port_range_max": "Port Range ending point here" } |
| Protocol | { "protocol": "Allowed Protocols here" } |
| Direction | { "direction": "Ingress/Egress" } |
| Security Rule ID | { "rule_id": "ID of a pre-existing Security Group Rule here" } |

**Allowed Protocols are: [None, 'ah', 'dccp', 'egp', 'esp', 'gre', 'hopopt', 'icmp', 'igmp', 'ip', 'ipip', 'ipv6-encap', 'ipv6-frag', 'ipv6-icmp', 'icmpv6', 'ipv6-nonxt', 'ipv6-opts', 'ipv6-route', 'ospf', 'pgm', 'rsvp', 'sctp', 'tcp', 'udp', 'udplite', 'vrrp']**

In order to use these endpoints, one must follow these steps: 
- Create a user, whose credentials would be used to make API Requests.
- Start the Django Server from within the folder named as "backend"
- Update "clouds.yaml" for OpenStack credentials

## Development

Want to contribute? Great!
> OpenYmir is still in Development Phase, so help your mate to make this project better and efficient.
> Contact me at: jaiswalaj716@gmail.com

## Tech

OpenYmir uses a number of open source projects to work properly:

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [OpenStack SDK](https://docs.openstack.org/openstacksdk/latest/)

And of course OpenYmir itself is open source.

## License
MIT

**Is this Free, Hell Yeah!**
