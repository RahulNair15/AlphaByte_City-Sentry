from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    points = models.IntegerField(default=0)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='streetvigil_users'  # Custom reverse accessor name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='streetvigil_users'  # Custom reverse accessor name
    )


class CapturedImage(models.Model):
    image = models.ImageField(upload_to='captured_images/')
    category = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(default='No description provided')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    status = models.CharField(max_length=4, default='P')
    rewards = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report #{self.id} - {self.category}"

    class Meta:
        ordering = ['-created_at']
