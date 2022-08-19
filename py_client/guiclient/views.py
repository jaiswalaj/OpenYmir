from re import template
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .endpoints import *
from .credentials import *
import requests

user_auth_details = user_auth_details = requests.auth.HTTPBasicAuth(username, password)

def server_list(request):
    servers = requests.get(parent_endpoint+server_list_endpoint, auth = user_auth_details).json()
    context = {
        "servers" : servers
    }
    return render(request, "guiclient/server.html", context)

def allocate_floating_ip(request, pk):
    response_received = requests.put(parent_endpoint+server_list_endpoint+pk+"/"+server_allocate_floating_ip_endpoint, auth = user_auth_details)
    return redirect("guiclient:servers")

def start_server(request, pk):
    response_received = requests.put(parent_endpoint+server_list_endpoint+pk+"/"+server_start_endpoint, auth = user_auth_details)
    return redirect("guiclient:servers")

def stop_server(request, pk):
    response_received = requests.put(parent_endpoint+server_list_endpoint+pk+"/"+server_stop_endpoint, auth = user_auth_details).json()
    return redirect("guiclient:servers")
    
    

