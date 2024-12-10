from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth.decorators import login_required

from feedback.models import Feedback
from .forms import FeedbackForm

@login_required
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.giver = request.user
            fb.save()
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, 'give_feedback.html', {'form': form})

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(receiver=request.user)
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})
