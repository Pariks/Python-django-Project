from django.db import models
from locality.models import Country, Territory
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField

# Create your models here.

class Investor(models.Model):
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
    
    user = models.ForeignKey(User)
    
    date_of_birth = models.DateField()
    phone_number =  models.CharField(max_length=50)
    cell_number =  models.CharField(max_length=50)
    
    country = models.ForeignKey(Country)
    territory = models.ForeignKey(Territory, blank=True, null=True)
    
    address = models.CharField(max_length=100)
    postal_code =  models.CharField(max_length=6, blank=True)
    city =  models.CharField(max_length=50)
    
    amount = models.IntegerField()
    approved = models.BooleanField(default=False)
    investment_timeframe = models.CharField(max_length=2,
                                      choices=TIMEFRAME_CHOICES)
    distribution = models.CharField(max_length=2,
                                      choices=DISTRIBUTION_CHOICES)
    submission_date =  models.DateTimeField(default=datetime.now, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
class InvestorRelation(models.Model):

    content = HTMLField(blank = True)