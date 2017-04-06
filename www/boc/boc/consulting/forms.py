from django.contrib.auth.models import User                                                                                                
from django.utils.translation import ugettext_lazy as _
from django import forms
from clever_selects.forms import ChainedChoicesModelForm, ChainedModelChoiceField
from django.core.urlresolvers import reverse_lazy
from consulting.models import ScheduleConsultation
import datetime
from django import forms


class ScheduleConsultationForm(forms.ModelForm):                                                                                    
    first_name = forms.CharField(label=_("First Name"), min_length=2, max_length=50, required=True)
    last_name = forms.CharField(label=_("Last Name"), min_length=2, max_length=50, required=True)
    phone = forms.CharField(label=_("Phone"), min_length=6, max_length=50, widget=forms.TextInput(attrs={'placeholder': '(###) ###-####'}), required=True)
    matter = forms.CharField(label=_("What are you looking to get out of the appointment?"), required=True, widget=forms.Textarea)
    date = forms.DateField(label=_("Select a Date"))
    class Meta:
        fields = '__all__'
        model = ScheduleConsultation


    def __init__(self, *args, **kwargs):
        super(ScheduleConsultationForm, self).__init__(*args, **kwargs) 

