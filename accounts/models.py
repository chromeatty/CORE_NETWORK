from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('requester', 'Requester'),
        ('provider', 'Provider'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    # add additional fields in here as name and email are not included in the AbstractUser model
    name = models.CharField(max_length=255, null=True, blank=True)  # Adding a name field
    email = models.EmailField(unique=True)

class Profile(models.Model):
    LOCATION_CHOICES = [
        ('address', 'Address'),
        ('coordinates', 'Latitude and Longitude'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.TextField(blank=True)
    service_areas = models.CharField(max_length=255, blank=True)
    preferences = models.TextField(blank=True)
    privacy_settings = models.BooleanField(default=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='address')
    address = models.CharField(
        max_length=255,
        blank=True,
        default="No address provided"
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        default=51.99656842422461
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        default=-0.9913942306871908
    )

    def __str__(self):
        return f"{self.user.username}'s profile"