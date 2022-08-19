from django.urls import path

from . import views

app_name = "guiclient"

urlpatterns = [
    path('', views.server_list, name='servers'),
    path('<slug:pk>/start-server/', views.start_server, name='start-server'),
    path('<slug:pk>/stop-server/', views.stop_server, name='stop-server'),
    path('<slug:pk>/allocate-floating-ip-to-server/', views.allocate_floating_ip, name='allocate-floating-ip'),
]