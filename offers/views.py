#from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .forms import OfferForm
from .models import Offer
from django.http import JsonResponse

# get all the requests from requests_app.models
#from django.contrib import messages # to display messages to the user


@login_required
def create_offer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            new_offer = form.save(commit=False)
            new_offer.user = request.user
            new_offer.save()
            # Redirect to view the offer list after creating the offer
            return redirect('user_offer_list')
    else:
        form = OfferForm()  
    return render(request, 'create_offer.html', {'form': form})


# to display the list of offers provided by the user only!!
@login_required
def user_offer_list(request):
    offers = Offer.objects.filter(user=request.user)
    return render(request, 'user_offer_list.html', {'offers': offers})

# to display the details of the offer provided by the user only!!
@login_required
def user_offer_details(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'user_offer_details.html', {'offer': offer})

@login_required
def edit_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('user_offer_list')
    else:
        form = OfferForm(instance=offer)
    return render(request, 'edit_offer.html', {'form': form})

@login_required
def delete_offer(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        req = get_object_or_404(Offer, pk=pk, user=request.user)
        req.delete()
        return JsonResponse({"status": "success", "message": "Offer deleted successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)


from requests_app.models import Request


@login_required
def view_requests_and_accept(request):
    # include requests that have not been accepted by anyone
    open_requests = Request.objects.filter(accepted_by=None)
    return render(request, 'view_requests_and_accept.html', {'requests_app': open_requests})
@login_required
def view_accepted_requests(request):
    requests = Request.objects.filter(accepted_by=request.user)
    return render(request, 'view_accepted_requests.html', {'requests_app': requests})

@login_required
# ensuer to use request_ as request is a django variable!!!!!
def offers_view_requester_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    return render(request, 'offers_view_requester_detail.html', {'request_': req})

@login_required
def toggle_accept(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        request_id = request.POST.get('request_id')
        req = get_object_or_404(Request, id=request_id)
        if req.accepted_by == request.user:
            req.accepted_by = None  # Retract the acceptance if the same user tries to toggle it
            accepted = False
        else:
            req.accepted_by = request.user  # Set the user as the one who accepts the request
            accepted = True
        req.save()

        return JsonResponse({
            'status': 'success',
            'accepted': accepted,
            'accepted_by': req.accepted_by.username if req.accepted_by else None
        })

    return JsonResponse({
        'status': 'error',
        'error': 'Invalid request or not an AJAX request'
    }, status=400)



