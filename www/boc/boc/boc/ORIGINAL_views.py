from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from userprofile.forms import PhoneForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from userprofile.models import UserExtraInfo
from predictions.models import PredictionArticle
from news.models import Article
from boc.forms import ContactForm
from django.contrib.flatpages.models import FlatPage
from django.core.mail import send_mail
from django.template import RequestContext
from decimal import *
import stripe

import json

def home(request):
    next_prediction = PredictionArticle.next_prediction()
    last_prediction = PredictionArticle.last_prediction()
    phone_form = PhoneForm()
    
    predictions = []
    
   
    if next_prediction:
        for prediction in next_prediction:
            predictions.append(prediction)
    if last_prediction:
        for prediction in last_prediction:
            predictions.append(prediction)
        
    #past_predictions = Prediction.objects.filter(open=True).order_by('-event__date')[:1]
    #upcoming_predictions = Prediction.objects.filter(open=False).order_by('-event__date')[:1]
  
    articles = Article.objects.filter(published=True).order_by('-date_published')[:4]
    c = {'articles': articles, 'predictions': predictions, 'phone_form': phone_form}
    return render(request, 'boc/home.html', c)

def login(request):
    form = AuthenticationForm(auto_id='id_%s-L')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST, auto_id='id_%s-L')
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST.get('next'))
        
    c = {'form': form, 'next':  '/'}
    return render(request, 'boc/login.html', c)

   
def join(request):
    
    form = ExtendedUserCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            user = auth.authenticate(username=cd['username'], password=cd['password1'])
            auth.login(request, user)
            UserExtraInfo.objects.create(user=user)
            return HttpResponseRedirect(request.POST.get('next'))
    c = {'form': form, 'next': '/'}
    return render(request, 'boc/join.html', c)

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect( '/')

def settings(request):
    if request.user.is_authenticated():
        c = {}
        return render(request, 'boc/settings.html', c)
    return HttpResponseRedirect( '/login/')



def contact(request):
    contact_flatpage = get_object_or_404(FlatPage, url='/contact/')
    form = ContactForm(request.POST or None)
    sent = False
    
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
    
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            recipients = ['info@betoncombat.com']
            
            send_mail(subject, message, email, recipients)
            form = ContactForm()
            sent = True
    
    
    c = {'form': form, 'flatpage': contact_flatpage, 'sent':sent}
    
    return render(request, 'flatpages/contact.html',  c)

def _ajax_response(request, template, **kwargs):
    response = {
        "html": render_to_string(
            template,
            RequestContext(request, kwargs)
        )
    }
    if "location" in kwargs:
        response.update({"location": kwargs["location"]})
    return HttpResponse(json.dumps(response), content_type="application/json")

def about(request):
    #/about/advisory-board/
    #/about/philosophy/
    #/about/the-brand/
    #/about/the-fund/
    #/about/word-from-the-founder/
    advisory = get_object_or_404(FlatPage, url='/about/advisory-board/')
    philosophy = get_object_or_404(FlatPage, url='/about/philosophy/')
    brand = get_object_or_404(FlatPage, url='/about/the-brand/')
    fund = get_object_or_404(FlatPage, url='/about/the-fund/')
    founder = get_object_or_404(FlatPage, url='/about/word-from-the-founder/')
    

    
    c = {'advisory': advisory, 'philosophy': philosophy, 'brand': brand,'fund':fund, 'founder':founder}
    
    return render(request, 'flatpages/about.html',  c)

def betting_guide(request):
    betting_guide = get_object_or_404(FlatPage, url='/betting-guide/guide/')
    c = {'betting_guide': betting_guide}
    
    return render(request, 'flatpages/betting-guide.html',  c)


def legal(request):
    privacy = get_object_or_404(FlatPage, url='/legal/privacy-policy/')
    terms = get_object_or_404(FlatPage, url='/legal/terms-and-conditions/')

    c = {'privacy': privacy, 'terms': terms}
    
    return render(request, 'flatpages/legal.html',  c)
    
    
