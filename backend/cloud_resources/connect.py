import openstack

openstack.enable_logging(debug=True)
conn = openstack.connection.from_config()