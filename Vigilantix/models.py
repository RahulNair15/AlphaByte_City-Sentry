from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    aadhaar = models.IntegerField(null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"



class PolicStation(models.Model):
    name = models.CharField(max_length=30, default="na")
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
    

class SecurityCamera(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"