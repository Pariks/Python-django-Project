from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Statistic(models.Model):
    year = models.IntegerField() 
    win = models.IntegerField()
    lost = models.IntegerField()
    risk = models.DecimalField(max_digits=12, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    fund = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    
    def __unicode__(self):
        return str(self.year)
    
    
class StatisticsContent(models.Model):
    content = HTMLField()
    