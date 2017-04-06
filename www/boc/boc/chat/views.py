import json
# import urllib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.shortcuts import render
from chat.models import ChatMessage
from django.core.urlresolvers import reverse

# from django.shortcuts import render
# from Crypto.Cipher import AES
# import binascii
# import hashlib


@csrf_exempt
def index(request):
    return render(request, 'chat/chat_room.html')

@csrf_exempt
def auth(request):
    response_data = {}
    try:
        if request.method == 'POST':
            sessionid = request.POST.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)
        response_data['user'] = {'username': user.username,'id': str(user.id)}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception:
        response_data['user'] = "error"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def message(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            text = request.POST.get('text')
            chat_message = ChatMessage(user=request.user, text=text)
            chat_message.save()
            return HttpResponse()
        
def chat_sound(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            request.user.userextrainfo.chat_sound = not request.user.userextrainfo.chat_sound
            request.user.save()
            return HttpResponse()
        
    
    
