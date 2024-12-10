from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RequestForm
from .models import Request
#from django.contrib import messages
from django.http import JsonResponse

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            # create a new request object but do not save it yet
            new_request = form.save(commit=False)
            # set the user of the request object to the current user
            new_request.user = request.user
            new_request.save()
            # redirect to the user_request_list view after creating the request
            return redirect('user_request_list')
    else:
        form = RequestForm()  

    return render(request, 'create_request.html', {'form': form})

@login_required
def user_request_list(request):
    req = Request.objects.filter(user=request.user)
    return render(request, 'user_request_list.html', {'requests_app': req})

@login_required
def user_request_details(request, pk):
    req = get_object_or_404(Request, pk=pk)
    return render(request, 'user_request_details.html', {'request_': req})

@login_required
def edit_request(request, pk):
    req = get_object_or_404(Request, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('user_request_list')
    else:
        form = RequestForm(instance=req)
    return render(request, 'edit_request.html', {'form': form})

@login_required
def delete_request(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        req = get_object_or_404(Request, pk=pk, user=request.user)
        req.delete()
        return JsonResponse({"status": "success", "message": "Request deleted successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)


# This is to allow requesers to view offers and like/ save what they have seen
from offers.models import Offer

@login_required
def requester_view_offers_detail(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    return render(request, 'requester_view_offers_detail.html', {'offer': offer})

@login_required
def requester_view_offers(request):
    offers = Offer.objects.all()
    return render(request, 'requester_view_offers.html', {'offers': offers})

@login_required
@login_required
def requester_liked_offers(request):
    offers = Offer.objects.filter(likes=request.user)
    return render(request, 'requester_liked_offers.html', {'offers': offers})

@login_required
def toggle_like(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        offer_id = request.POST.get('offer_id')
        offer = get_object_or_404(Offer, id=offer_id)
        liked = request.user in offer.likes.all()

        if liked:
            offer.likes.remove(request.user)
        else:
            offer.likes.add(request.user)
        
        return JsonResponse({
            'status': 'success',
            'liked': not liked,
            'likes_count': offer.likes.count()
        })

    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request or not an AJAX request'
    }, status=400)