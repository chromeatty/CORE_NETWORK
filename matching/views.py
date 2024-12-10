from django.shortcuts import render
from matching.utils import match_requests_offers
def view_matches(request):
    matches = match_requests_offers()
    return render(request, 'matches.html', {'matches': matches})
