from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class  AdvisoryBoard(models.Model):

    title = models.TextField(blank=True)
    content = HTMLField()
    image =  models.ImageField(upload_to = 'media/carousel/', blank=True)
    order = models.IntegerField()

    def __unicode__(self):

        return self.title