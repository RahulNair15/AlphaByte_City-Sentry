from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Vigilantix.models import *


admin.site.register(CustomUser)
admin.site.register(PolicStation)
admin.site.register(SecurityCamera)
# Register your models here.
