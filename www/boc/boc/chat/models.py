from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ChatMessage(models.Model):

    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text