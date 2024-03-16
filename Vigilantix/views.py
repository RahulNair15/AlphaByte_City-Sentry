from django.db import IntegrityError
from django.urls import reverse
import folium
from folium.plugins import MousePosition
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponseRedirect, JsonResponse
import openrouteservice
import operator
from functools import reduce
from django.contrib.auth import authenticate, login, logout
from .models import PolicStation,SecurityCamera,CustomUser
import http.client


# def index(request):
#     return render(request,"Vigilantix/landingpage.html")

def landingpage(request):
    return render(request,"Vigilantix\landingpage.html")

def search(request):
    latitude = 27.030703
    longitude = 75.893527
    cradius = 5.0
    # Define the map center
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        cradius = float(request.POST.get('radius'))
    center = [latitude, longitude]

    #creating map
    m = folium.Map(location=center, zoom_start=13)
    folium.LatLngPopup().add_to(m)

    #adding user to map
    tooltip = "Your Location"
    icon=folium.Icon(color='red', prefix='fa', icon='user')
    folium.Marker(location=center, tooltip=tooltip, icon=icon).add_to(m)
    folium.Circle(
        location=center,
        radius=cradius*1000,
        fill=True,
        fill_opacity=0.1,
        color='green'
    ).add_to(m)

    stations = PolicStation.objects.all()
    cameras = SecurityCamera.objects.all()
    radius = cradius  # radius in kilometers
    for station in stations:
        station_latitude = station.latitude
        station_longitude = station.longitude
        dist = haversine(latitude, longitude,station_latitude, station_longitude)
        if dist <= radius:
            marker_location = (station_latitude, station_longitude)
            tooltip = station.name
            icon=folium.Icon(color='blue', prefix='fa',icon='shield')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)
    for camera in cameras:
        camera_latitude = camera.latitude
        camera_longitude = camera.longitude
        dist = haversine(latitude, longitude,camera_latitude, camera_longitude)
        if dist <= radius:
            marker_location = (camera_latitude, camera_longitude)
            tooltip = "Camera"+str(camera.id)
            icon=folium.Icon(color='green', prefix='fa',icon='video-camera')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)
    
    m=m._repr_html_() #updated
    context = {'my_map': m,
                'latitudef':latitude,
                'longitudef':longitude,
                'radiusf':cradius,
               }
    return render(request, 'Vigilantix/map.html', context)

def routing(request):
    latitudefrom = 19.09949
    longitudefrom = 72.86476
    latitudeto = 19.07755
    longitudeto = 72.86591

    # Define the start and end coordinates
    start = (latitudefrom, longitudefrom) 
    end = (latitudeto, longitudeto) 

    # Create the map
    m = folium.Map(location=start, zoom_start=13 , height="100%" )
    folium.LatLngPopup().add_to(m)
    # folium.TileLayer('stamentoner').add_to(m)
    # Add the start and end markers
    folium.Marker(location=start, tooltip='Start').add_to(m)
    folium.Marker(location=end, tooltip='End').add_to(m)

    if request.method == 'POST':
        latitudefrom = float(request.POST.get('latitudefrom'))
        longitudefrom = float(request.POST.get('longitudefrom'))
        latitudeto = float(request.POST.get('latitudeto'))
        longitudeto = float(request.POST.get('longitudeto'))

    m = folium.Map(location=list(reversed([longitudefrom, latitudefrom])), zoom_start=13)
    coords = [[longitudefrom, latitudefrom], [longitudeto, latitudeto]]
    ors_client = openrouteservice.Client(key='5b3ce3597851110001cf6248844ba845bb7648a3bda6b57313f08c0d')

    route = ors_client.directions(coordinates=coords,
                        profile='foot-walking',
                        format='geojson')
    waypoints = list(dict.fromkeys(reduce(operator.concat, list(map(lambda step: step['way_points'], route['features'][0]['properties']['segments'][0]['steps'])))))
    folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']], color="green").add_to(m)
    cradius = 30
    
    stations = PolicStation.objects.all()
    cameras = SecurityCamera.objects.all()
    radius = cradius  # radius in kilometers
    for station in stations:
        station_latitude = station.latitude
        station_longitude = station.longitude
        dist = haversine(latitudefrom, longitudefrom,station_latitude, station_longitude)
        if dist <= radius:
            marker_location = (station_latitude, station_longitude)
            tooltip = station.name
            icon=folium.Icon(color='blue', prefix='fa',icon='shield')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)
        dist = haversine(latitudeto, longitudeto,station_latitude, station_longitude)
        if dist <= radius:
            marker_location = (station_latitude, station_longitude)
            tooltip = station.name
            icon=folium.Icon(color='blue', prefix='fa',icon='shield')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)
    for camera in cameras:
        camera_latitude = camera.latitude
        camera_longitude = camera.longitude
        dist = haversine(latitudefrom, longitudefrom,camera_latitude, camera_longitude)
        if dist <= radius:
            marker_location = (camera_latitude, camera_longitude)
            tooltip = "Camera"+str(camera.id)
            icon=folium.Icon(color='green', prefix='fa',icon='video-camera')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)
        dist = haversine(latitudeto, longitudeto,camera_latitude, camera_longitude)
        if dist <= radius:
            marker_location = (camera_latitude, camera_longitude)
            tooltip = "Camera"+str(camera.id)
            icon=folium.Icon(color='green', prefix='fa',icon='video-camera')
            folium.Marker(location=marker_location, tooltip=tooltip, icon=icon).add_to(m)

    m=m._repr_html_() #updated
    context = {'my_map': m,
                'latitudefrom' : latitudefrom,
                'longitudefrom' : longitudefrom,
                'latitudeto' : latitudeto,
                'longitudeto' : longitudeto,
               }
    return render(request,"Vigilantix/routing.html",context)

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_location(request):
    if request.method == 'POST':
        # Extract the position data from the request body
        data = json.loads(request.body.decode('utf-8'))
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        print(latitude, longitude, data)

        # Do something with the position data
        # ...
        
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})\
            
def police(request):
    if request.method == 'POST':
        name = request.POST.get('psname')
        latitude = request.POST.get('pslat')
        longitude = request.POST.get('pslon')
        selection = request.POST.get('selection')
        print("user selected "+selection)
        if selection == '1':
            polobj = PolicStation(name=name,latitude=latitude,longitude=longitude)
            polobj.save()
        elif selection == '0':
            polobj = SecurityCamera(latitude=latitude,longitude=longitude)
            polobj.save()
    return render(request, 'Vigilantix/police.html',{
        'policelist':PolicStation.objects.all().reverse()
    })


def cammera(request):
    if request.method == 'POST':
        latitude = request.POST.get('cmlat')
        longitude = request.POST.get('cmlon')
        polobj = SecurityCamera(latitude=latitude,longitude=longitude)
        polobj.save()
    return render(request, 'Vigilantix/cammera.html',{
        'camlist':SecurityCamera.objects.all()
    })


def contact(request):
     return render(request, 'Vigilantix/contact.html')


def register(request):
    if request.method == "GET":
        return render(request, "Vigilantix/users.html")
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        aadhar = request.POST["aadhar"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        try:
            # Aadhar authentication
            conn = http.client.HTTPSConnection("api.apyhub.com")

            payload = "{\n    \"aadhaar\":\""+aadhar+"\"\n}"

            headers = {
                'apy-token': "APY0W3pTpUGPtk9Bi5DpOENp0Fri0quMrLFoyA4Id7OcO3kRQplqHCl4KNz4mNzZo1E8FUz",
                'Content-Type': "application/json"
                }
            conn.request("POST", "/validate/aadhaar", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))

            json_data = json.loads(data.decode("utf-8"))
            result = json_data["data"]

            print(result)
            # Attempt to create new user

            if result == True:
                try:
                    user = CustomUser.objects.create(email=email, first_name=firstname, last_name=lastname, aadhaar=aadhar, password=password)
                    user.save()
                except IntegrityError:
                    return render(request, "Vigilantix/users.html", {
                        "message": "Username already taken."
                    })
                login(request, user)
                return HttpResponseRedirect(reverse("index1"))
        except:   
            return render(request, "Vigilantix/users.html", {
                    "message": "Invalid AADHAAR Check once and try Again"
                    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        first_name = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=first_name, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index1"))
        else:
            return render(request, "Vigilantix/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Vigilantix/login1.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index1"))
