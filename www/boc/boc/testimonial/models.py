from __future__ import unicode_literals

from django.db import models
from tinymce.models import HTMLField
from django.core.urlresolvers import reverse

# Create your models here.

class TestimonialItem(models.Model):
    content = HTMLField(blank=True)
    name = models.TextField(blank=True)
    order = models.IntegerField()
    video = models.FileField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        reverse("testimonials:detail", kwargs={"id":self.id})


    class Meta:
        ordering = ["-order"]
