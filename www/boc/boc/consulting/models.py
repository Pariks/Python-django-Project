from django.db import models

from tinymce.models import HTMLField

# Create your models here.
class SubscriptionInfo(models.Model):
    DURATION = (
            ('W', 'weekly'),
            ('M', 'monthly'),
            ('Y', 'annually')
        )
    duration = models.CharField(max_length=1, choices=DURATION, primary_key=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=25)
    def __unicode__(self):
        return self.duration

class Benefit(models.Model):
    subscriptonType = models.ForeignKey(SubscriptionInfo, on_delete=models.CASCADE, default='')
    description = HTMLField(blank=True)


class ScheduleConsultation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=300)
    matter = models.TextField()
    date = models.DateField()
    start_time_1 = models.TimeField()
    start_time_2 = models.TimeField()
    start_time_3 = models.TimeField()

