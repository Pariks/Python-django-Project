from django.db import models

# Create your models here.

class CarouselItem(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('VI', 'Video'),
        ('IM', 'Image')
    )
    BUTTON_CHOICES = (
        ('JOIN NOW', 'JOIN NOW'),
        ('READ MORE', 'READ MORE'),
        ('LEARN MORE', 'LEARN MORE'),
        ('APPLY NOW', 'APPLY NOW')
    )
    
    SHOW_OR_HIDE_BUTTON_CHOICES = (
        ('SHOW BUTTON', 'SHOW BUTTON'),
        ('HIDE BUTTON', 'HIDE BUTTON')
    )
    title = models.TextField(blank=True) 
    subtitle = models.TextField(blank=True)
    order = models.IntegerField()
    type = models.CharField(max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    buttons = models.CharField(max_length=20, choices=BUTTON_CHOICES, blank=True)
    show_or_hide_button = models.CharField(max_length=20, choices=SHOW_OR_HIDE_BUTTON_CHOICES)
    link = models.TextField(blank=True)
    image =  models.ImageField(upload_to = 'media/carousel/', blank=True)
    video_url = models.CharField(max_length=200, blank=True)
    
    
    def __unicode__(self):
        return self.title


class FundsUnderManagement(models.Model):
    amount = models.FloatField()
    def __unicode__(self):
        return str(self.amount)
