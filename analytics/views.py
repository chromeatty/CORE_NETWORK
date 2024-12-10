from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseForbidden
from requests_app.models import Request
from django.shortcuts import render

@login_required
def dashboard(request):
    if request.user.is_staff or request.user.user_type == 'provider':
        total_requests = Request.objects.count()
        fulfilled_requests = Request.objects.filter(status='accepted').count()
        category_counts = Request.objects.values('category').annotate(count=Count('category'))
        context = {
            'total_requests': total_requests,
            'fulfilled_requests': fulfilled_requests,
            'category_counts': category_counts,
        }
        return render(request, 'dashboard.html', context)
    else:
        return HttpResponseForbidden("You do not have access to this page.")
