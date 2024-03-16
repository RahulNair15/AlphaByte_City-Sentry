from django.urls import path,re_path
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'Vigilantix'  # Define the namespace here

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("search", views.search, name="search"),
    path("routing", views.routing, name="routing"),
    path("police", views.police, name="police"),
    path("cammera", views.cammera, name="cammera"),
    path("contact", views.contact, name="contact"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("getLocation",views.get_location, name= "getLocation")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)