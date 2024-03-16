from django.urls import path
from . import views

app_name = 'wastesegregation'  # Define the app namespace

urlpatterns = [
    path('', views.index2, name='index2'),  # Maps the root URL to the index view
    path('ws/', views.websocket_endpoint),  # Maps the /ws URL to the websocket_endpoint view
]
