from django.shortcuts import render
from investor.forms import InvestorApplicationForm, InvestForm
from django.views.generic.detail import BaseDetailView
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from locality.models import Territory, Country
from django.http import HttpResponseRedirect, HttpResponse
from allauth.account.forms import SignupForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from decimal import Decimal
from payments.models import Customer
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe
import json
from investor.models import InvestorRelation
# Create your views here.

def index(request):
    title = 'Investment Application Form'
    if request.user.is_authenticated():
        user = request.user
        investor = user.investor_set.all()
        form = InvestorApplicationForm(request.POST or None)
        if len(investor) > 0:
            if investor[0].approved:
                form = InvestForm(request.POST or None)
                title = 'Invest'
                if request.method == 'POST':
                    if form.is_valid():
                        cd = form.cleaned_data
                        try:
                            customer = request.user.customer
                        except ObjectDoesNotExist:
                            customer = Customer.create(request.user)
                        customer.update_card(request.POST.get("stripe_token"))
                        amount = Decimal(cd["amount"])
                        response = {}
                        customer.charge(amount)
                        try:
                            #customer.charge(amount)
                            response.update({"location": reverse('investor:success')})
                        except:
                            response.update({"location": reverse('investor:failure')})
                            
                        return HttpResponse(json.dumps(response), content_type="application/json")
                        
        else:
            if request.method == 'POST':
                if form.is_valid():
                    # Create, but don't save the new investor instance.
                    investor = form.save(commit=False)
                    investor.user = user  # add user to investor
                    investor.save() # Save the new instance.
                    form.save_m2m() # Now, save the many-to-many data for the form.
                    
                    #save firstname and lastname
                    cd = form.cleaned_data
                    user.first_name = cd['first_name']
                    user.last_name = cd['last_name']
                    user.save()
                    
                    #send email to us about new investor
                    msg_html = render_to_string('investor/_email.html', {'investor': investor, 'user':user})
                    send_mail('New Investor', '', 'info@betoncombat.com', ['ryan.cimoszko@gmail.com','info@betoncombat.com'],  html_message=msg_html, fail_silently=True)
                    
                    return HttpResponseRedirect(request.POST.get('next'))
         
    else:
        form = SignupForm(request.POST or None, request.FILES or None)
        
    investor_relation = InvestorRelation.objects.filter().order_by('id')
    is_active = 1
    
    c = {'form': form, 'next': '/investing/', 'title':title,  'investor_relation': investor_relation, 'is_active': is_active}   
    return render(request, 'investor/investing.html', c)
        

class CountryChainedView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        field = request.GET.get('field')
        parent_value = request.GET.get("parent_value")
        country = Country.objects.filter(pk=parent_value)
        territories = Territory.objects.filter(country=country)
        name_list = []
        id_list = []
        for territory in territories:
            name_list.append(territory.name)
            id_list.append(territory.id)
        
        choices = tuple(zip(id_list, name_list))
        return JsonResponse(choices, safe=False)

def success(request):
    return render(request, 'investor/invest-success.html')

def failure(request):
    return render(request, 'investor/invest-failure.html')


def switch(request):
    title = 'Investment Application Form'
    if request.user.is_authenticated():
        user = request.user
        investor = user.investor_set.all()
        form = InvestorApplicationForm(request.POST or None)
        if len(investor) > 0:
            if investor[0].approved:
                form = InvestForm(request.POST or None)
                title = 'Invest'
                if request.method == 'POST':
                    if form.is_valid():
                        cd = form.cleaned_data
                        try:
                            customer = request.user.customer
                        except ObjectDoesNotExist:
                            customer = Customer.create(request.user)
                        customer.update_card(request.POST.get("stripe_token"))
                        amount = Decimal(cd["amount"])
                        response = {}
                        customer.charge(amount)
                        try:
                            #customer.charge(amount)
                            response.update({"location": reverse('investor:success')})
                        except:
                            response.update({"location": reverse('investor:failure')})

                        #return HttpResponse(json.dumps(response), content_type="application/json")

        else:
            if request.method == 'POST':
                if form.is_valid():
                    # Create, but don't save the new investor instance.
                    investor = form.save(commit=False)
                    investor.user = user  # add user to investor
                    investor.save() # Save the new instance.
                    form.save_m2m() # Now, save the many-to-many data for the form.

                    #save firstname and lastname
                    cd = form.cleaned_data
                    user.first_name = cd['first_name']
                    user.last_name = cd['last_name']
                    user.save()

                    #send email to us about new investor
                    msg_html = render_to_string('investor/_email.html', {'investor': investor, 'user':user})
                    send_mail('New Investor', '', 'info@betoncombat.com', ['ryan.cimoszko@gmail.com','info@betoncombat.com'],  html_message=msg_html, fail_silently=True)

                    return HttpResponseRedirect(request.POST.get('next'))

    else:
        form = SignupForm(request.POST or None, request.FILES or None)

    investor_relation = InvestorRelation.objects.filter().order_by('id')
    is_active = 1

    c = {'form': form, 'next': '/investing/', 'title':title, 'investor_relation': investor_relation, 'is_active': is_active }
    return render(request, 'investor/switch_tab.html', c)

