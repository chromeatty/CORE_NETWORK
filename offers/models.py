from django.db import models
from accounts.models import User
from django.utils import timezone

class Offer(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('water', 'Water'),
        ('clothing', 'Clothing'),
        ('shelter', 'Shelter'),
        ('medical', 'Medical Supplies'),
        ('other', 'Other'),
        
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    LOCATION_CHOICES = (
        ('address', 'Address'),
        ('coordinates', 'Latitude and Longitude'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='No title given')
    description = models.TextField(default='No description given')
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='address')
    address = models.CharField(
        max_length=255,
        blank=True,
        default="No address provided"
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        default=None
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        default=None
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='Pending')
    quantity = models.IntegerField(default=1)
    availability_start = models.DateTimeField(default=timezone.now)
    availability_end = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_offers', blank=True)

    def __str__(self):
        return self.title
