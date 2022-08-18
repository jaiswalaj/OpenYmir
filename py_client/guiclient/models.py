from django.db import models

# Create your models here.

class Image(models.Model):
    image_id = models.CharField(max_length=50)
    image_name = models.CharField(max_length=20)
    image_status = models.CharField(max_length=10)

class Flavor(models.Model):
    flavor_id = models.CharField(max_length=50)
    flavor_name = models.CharField(max_length=20)

class Network(models.Model):
    network_id = models.CharField(max_length=50)
    network_name = models.CharField(max_length=20)

class Router(models.Model):
    router_id = models.CharField(max_length=50)
    router_name = models.CharField(max_length=20)
    external_gateway = models.BooleanField()

class Subnet(models.Model):
    subnet_id = models.CharField(max_length=50)
    subnet_name = models.CharField(max_length=20)
    subnet_cidr = models.CharField(max_length=20)
    network_id = models.ForeignKey(Network, on_delete=models.CASCADE)
    router_id = models.ForeignKey(Router, on_delete=models.DO_NOTHING)

class Server(models.Model):
    server_id = models.CharField(max_length=50)
    server_name = models.CharField(max_length=20)
    public_ip = models.GenericIPAddressField(null=True)
    private_ip = models.GenericIPAddressField(null=True)
    image_id = models.ForeignKey(Image, on_delete=models.DO_NOTHING)
    flavor_id = models.ForeignKey(Flavor, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10)
    network_id = models.ForeignKey(Network, on_delete=models.CASCADE)


