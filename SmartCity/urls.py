from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from Vigilantix import views as vigilantix_views

urlpatterns = [
    path('', vigilantix_views.landingpage, name='landingpage'),
    path('saferoute/', include('Vigilantix.urls')),
    path('traffic/', include('streetvigil.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('wastesegregation/', include('wastesegregation.urls')),
    path('chatbot/', include('Chatbot.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


