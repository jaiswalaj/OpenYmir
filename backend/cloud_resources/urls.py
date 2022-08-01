from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "resources"

urlpatterns = [
    path('<slug:pk>/', views.ResourceList.as_view()),
    path('<slug:pk>/<slug:pk2>/', views.ResourceDetail.as_view()),
    path('<slug:pk>/<slug:pk2>/<slug:pk3>/', views.ResourceUpdate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)