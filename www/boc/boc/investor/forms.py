from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django import forms
from locality.models import Country, Territory
from clever_selects.forms import ChainedChoicesModelForm, ChainedModelChoiceField
from django.core.urlresolvers import reverse_lazy
from investor.models import Investor
import datetime


class InvestorApplicationForm(ChainedChoicesModelForm):
    REINVEST = 'RE'
    CHEQUE = 'CH'
    DISTRIBUTION_CHOICES = (
        (REINVEST, 'Reinvest'),
        (CHEQUE, 'Cheque'))
    
    ONE = '12'
    TWO = '24'
    THREE = '36'
    
    TIMEFRAME_CHOICES = (
        (ONE, '12 Months'),
        (TWO, '24 Months'),
        (THREE, '36 Months'))
    
    first_name = forms.CharField(label=_("First Name"), min_length=2, max_length=50, required=True)
    last_name = forms.CharField(label=_("Last Name"), min_length=2, max_length=50, required=True)
    
    date_of_birth  = forms.DateField(label=_("Date of Birth"), widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), input_formats=['%Y-%m-%d'], required=True)
    phone_number = forms.CharField(label=_("Phone Number"), min_length=6, max_length=50, widget=forms.TextInput(attrs={'placeholder': '(###) ###-####'}), required=True)
    cell_number = forms.CharField(label=_("Cell Number"), min_length=6, max_length=50, widget=forms.TextInput(attrs={'placeholder': '(###) ###-####'}), required=True)
    

    country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), required=True,
        empty_label=_(u'Select a country'))
    territory = ChainedModelChoiceField(parent_field='country', ajax_url=reverse_lazy('investor:ajax_chained_country'),
        empty_label=_(u'Select a territory'), model=Territory, required=False)
    
    address = forms.CharField(label=_("Address"), min_length=8, max_length=100, required=True)
    postal_code = forms.CharField(label=_("Postal/Zip Code"), min_length=5, max_length=6, required=True)
    city = forms.CharField(label=_("City"), min_length=1, max_length=50, required=True)

    amount = forms.IntegerField(label=_("Amount ($USD)"), required=True)
    investment_timeframe = forms.ChoiceField(choices=TIMEFRAME_CHOICES, widget=forms.RadioSelect())
    distribution = forms.ChoiceField(choices=DISTRIBUTION_CHOICES, widget=forms.RadioSelect())
    
    class Meta:
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'city', 'country', 'territory', 'postal_code', 'phone_number',  'cell_number', 'amount', 'investment_timeframe', 'distribution']
        model = Investor
           
           
    def __init__(self, *args, **kwargs):
        super(InvestorApplicationForm, self).__init__(*args, **kwargs) 

class InvestForm(forms.Form):
    amount= forms.DecimalField(decimal_places=2, label="Amount (USD)")

