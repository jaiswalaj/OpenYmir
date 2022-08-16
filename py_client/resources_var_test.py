resources = [
    {
        "resource": "netork", 
        "details": [
            {
                "network_name": "net1",
                "subnet_cidr": "192.168.101.0/24",
            },
            {
                "network_name": "net2",
                "subnet_cidr": "192.168.102.0/24",
            },
            {
                "network_name": "net3",
                "subnet_cidr": "192.168.103.0/24",
            },
            {
                "network_name": "net4",
                "subnet_cidr": "192.168.104.0/24",
            },
        ]
    },
    {
        "resource": "router",
        "details": [
            {
                "router_name": "rou1",
                "external_gateway": True,
                "internal_interface": ["net2"],
            },
            {
                "router_name": "rou2",
                "external_gateway": False,
                "internal_interface": ["net1", "net3", "net4"],
            }
        ]
    },
    {
        "resource": "server",
        "details": [
            {
                "server_name": "ser1",
                "image_name": "cirros-0.5.2-x86_64-disk",
                "flavor_name": "m1.nano",
                "network_name": "net1",
                "floating_ip": True,
                "status": "ACTIVE",
            },
            {
                "server_name": "ser2",
                "image_name": "cirros-0.5.2-x86_64-disk",
                "flavor_name": "m1.nano",
                "network_name": "net2",
                "floating_ip": True,
                "status": "ACTIVE",
            },
            {
                "server_name": "ser3",
                "image_name": "cirros-0.5.2-x86_64-disk",
                "flavor_name": "m1.nano",
                "network_name": "net3",
                "floating_ip": True,
                "status": "ACTIVE",
            },
            {
                "server_name": "ser1-1",
                "image_name": "cirros-0.5.2-x86_64-disk",
                "flavor_name": "m1.nano",
                "network_name": "net1",
                "floating_ip": True,
                "status": "SHUTOFF",
            },
        ]
    }
]