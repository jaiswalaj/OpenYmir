from django.contrib import admin
from .models import Image, Flavor, Network, Router, Subnet, Server

# Register your models here.

admin.site.register(Image)
admin.site.register(Flavor)
admin.site.register(Network)
admin.site.register(Router)
admin.site.register(Subnet)
admin.site.register(Server)