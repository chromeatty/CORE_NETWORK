from django.shortcuts import render
def base(request):
    return render(request, 'base.html') 

from requests_app.models import Request

def home(request):
    # Fetch the 5 most recent requests, ordering by the `created_at` field in descending order
    recent_requests = Request.objects.order_by('-created_at')[:5]
    
    return render(request, 'home.html', {
        'recent_requests': recent_requests,
    })


def about_us(request):
    return render(request, 'about_us.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    return render(request, 'contact.html')