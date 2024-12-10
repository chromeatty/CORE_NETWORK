import django_filters
from .models import Request

class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ['title', 'description', 'location', 'category', 'urgency', 'status']
