from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class OpportunityItem(models.Model):

#    content = models.TextField(blank=True)
    title = models.TextField(blank=True)
    content = HTMLField(blank=True)
    image =  models.ImageField(upload_to = 'media/carousel/', blank=True)
    order = models.IntegerField()

    def __unicode__(self):

        return self.title