# OpenYmir
## Django Rest API based on OpenStack SDK



OpenYmir is built using Django Rest Framework and OpenStack SDK to provide  features through which one can perform various operations on OpenStack (an open standard cloud computing platform, mostly deployed as infrastructure-as-a-service). 

OpenYmir allows you to perform CRUD operations on Networks, Subnets, Routers, Servers, Security Groups, and Floating IPs. Some key highlights of the operations which can be performed using OpenYmir API calls are as follows:-

- Create, List, Retrieve, Delete, Start and Stop a Server
- Allocate Floating IP to a Server
- Delete a Network completely and safely ( i.e. deleting Servers on the Network but not Routers)
- Provide proper Exceptions in case of any failure

## API Endpoints
Following are the enpoints and the type of request which needs to make to perform various operations on OpenStack Cloud Platform. However, for the sake of ease Domain Name is being replaced by "127.0.0.1:8000" in the endpoints listed below.

List Resources (GET Request)
- http://127.0.0.1:8000/api/resources/servers/
- http://127.0.0.1:8000/api/resources/networks/
- http://127.0.0.1:8000/api/resources/subnets/
- http://127.0.0.1:8000/api/resources/images/
- http://127.0.0.1:8000/api/resources/flavors/
- http://127.0.0.1:8000/api/resources/routers/
- http://127.0.0.1:8000/api/resources/floating-ip/
- http://127.0.0.1:8000/api/resources/security-groups/

Create Resources (POST Request)
- Data Required for creating Server: Name, Image ID, Flavor ID, and Network ID
-- http://127.0.0.1:8000/api/resources/servers/
- Data Required for creating Network: Name
-- http://127.0.0.1:8000/api/resources/networks/
- Data Required for creating Subnet: Name, Network ID, and CIDR
-- http://127.0.0.1:8000/api/resources/subnets/
- Data Required for creating Router: Name
-- http://127.0.0.1:8000/api/resources/subnets/
- Data Required for creating Security Group: Name, and Description
-- http://127.0.0.1:8000/api/resources/security-groups/

Retrieve Details (GET Request) and Destroy (DELETE Request) a Resource
- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/
- http://127.0.0.1:8000/api/resources/networks/"Network ID Here"/
- http://127.0.0.1:8000/api/resources/subnets/"Subnet ID Here"/
- http://127.0.0.1:8000/api/resources/images/"Image ID Here"/
- http://127.0.0.1:8000/api/resources/flavors/"Flavor ID Here"/
- http://127.0.0.1:8000/api/resources/routers/"Router ID Here"/
- http://127.0.0.1:8000/api/resources/floating-ip/"Floating IP ID Here"/
- http://127.0.0.1:8000/api/resources/security-groups/"Security Group ID Here"/

Update (PUT Request) a Resource
- Data Required to start a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/start
- Data Required to stop a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/stop
- Data Required to allocate a Floating IP to a Server: None
-- http://127.0.0.1:8000/api/resources/servers/"Server ID Here"/allocate-floating-ip
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