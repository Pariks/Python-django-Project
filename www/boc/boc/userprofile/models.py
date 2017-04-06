from django.db import models
from django.contrib.auth.models import User
from payments.models import Customer
import decimal
import stripe

# Create your models here.
class PhoneNumber(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    phone_number =  models.BigIntegerField(unique=True)
    sent = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s" % self.phone_number

    
class UserExtraInfo(models.Model):
    AMERICAN = 'AM'
    DECIMAL = 'DE'
    PROB = 'PR'
    RETURN = 'RE'
    
    ODDS_TYPE_CHOICES = (
                   (AMERICAN, 'American'),
                   (DECIMAL, 'Decimal'),
                   (PROB, 'Implied Probability'),
                   (RETURN, 'Return On'),
                   )
    
    user = models.OneToOneField(User)
    #date_of_birth = models.DateField()
    #address = models.CharField(max_length=100)
    #postal_code =  models.CharField(max_length=6)
    #city =  models.CharField(max_length=50)
    #province =  models.CharField(max_length=50)
    #phone_number =  models.BigIntegerField(max_length=100)
    #mothers_maiden_name =  models.CharField(max_length=50)
    #city_of_birth = models.CharField(max_length=50)
    investor = models.BooleanField(default=False)
    chat_sound = models.BooleanField(default=True)
    odds_format = models.CharField(max_length=2, choices=ODDS_TYPE_CHOICES, blank=True, default=AMERICAN)
    amount = models.IntegerField(default=10)
    news_letter = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "Extra info for %s" % (self.user)      


class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar')


class UserFollowedBy(models.Model):
    user = models.ForeignKey(User)
    followed_by = models.ForeignKey(User, related_name="user_following")
