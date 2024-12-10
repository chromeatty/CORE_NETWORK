from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User
from .forms import MessageForm
from .models import Message

@login_required
def send_message(request, recipient_id=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect('inbox')
    else:
        initial = {}
        if recipient_id:
            initial['recipient'] = User.objects.get(pk=recipient_id)
        form = MessageForm(initial=initial)
    return render(request, 'send_message.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def send_message_to(request, recipient_id):
    return send_message(request, recipient_id)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


@login_required
def delete_message(request, message_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        message = get_object_or_404(Message, pk=message_id, recipient=request.user)
        message.delete()
        return JsonResponse({"status": "success", "message": "Message deleted successfully."})
    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, recipient=request.user)
    return render(request, 'view_message.html', {'message': message})