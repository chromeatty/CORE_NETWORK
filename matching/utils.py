from requests_app.models import Request
from offers.models import Offer

def match_requests_offers():
    matches = []
    pending_requests = Request.objects.filter(status='pending')
    for req in pending_requests:
        possible_offers = Offer.objects.filter(
            category=req.category,
            availability_start__lte=req.created_at,
            availability_end__gte=req.created_at
        )
        if possible_offers.exists():
            match = {
                'request': req,
                'offers': possible_offers
            }
            matches.append(match)
    return matches
