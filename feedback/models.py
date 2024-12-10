from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    giver = models.ForeignKey(User, related_name='feedback_given', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='feedback_received', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    testimonial = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
