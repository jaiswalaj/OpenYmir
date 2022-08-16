resources = [
    {
        "name": "net1", 
        "subnet_cidr": "192.168.101.0/24",
        "router_name": "rou1",
        "server_details": [
            {"server_name": "ser1", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": True, "status": "active"}, 
            {"server_name": "ser2", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": False, "status": "active"}, 
            {"server_name": "ser3", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": True, "status": "shutoff"}
        ],
    },
    {
        "name": "net2", 
        "subnet_cidr": "192.168.102.0/24",
        "router_name": "rou1",
        "server_details": [
            {"server_name": "ser1", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": True, "status": "active"}, 
            {"server_name": "ser2", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": False, "status": "active"}, 
            {"server_name": "ser3", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": True, "status": "active"}
        ],
    },
    {
        "name": "net3", 
        "subnet_cidr": "192.168.103.0/24",
        "router_name": "rou1",
        "server_details": [
            {"server_name": "ser1", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": True, "status": "active"}, 
            {"server_name": "ser2", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.nano", "floating_ip": False, "status": "shutoff"}, 
            {"server_name": "ser3", "image_name": "cirros-0.5.2-x86_64-disk", "flavor_name": "m1.tiny", "floating_ip": True, "status": "shutoff"}
        ],
    },
]