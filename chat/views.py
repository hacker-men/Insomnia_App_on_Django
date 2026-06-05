from django.shortcuts import render
from chat.models import Message

def chat_view(request):
    messages = Message.objects.all()[:20]
    return render(request, "chat/index.html", {"messages": messages})
