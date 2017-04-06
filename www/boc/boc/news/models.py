from django.db import models
from mma.models import Sport, Event, Promotion, Fighter, Fight
from tinymce.models import HTMLField
import datetime
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.db import IntegrityError
from autoslug import AutoSlugField
from django.utils import timezone
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(User)
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/news', blank=True)
    content = HTMLField(blank=True)
    preview_content = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    
    date_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    date_published = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    event = models.ForeignKey(Event, null=True, blank=True)
    sport = models.ForeignKey(Sport, null=True, blank=True)
    promotion = models.ForeignKey(Promotion, null=True, blank=True)
    fight = models.ForeignKey(Fight, null=True, blank=True)
    fighter = models.ForeignKey(Fighter, null=True, blank=True)
    
    slug = AutoSlugField(populate_from='title', editable=True)

    @models.permalink
    def get_absolute_url(self):
        return 'news:article', (), {'slug': self.slug}
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title
"""    
def update_published_date(sender, instance, **kwargs):
    if instance.published:
        instance.date_published = datetime.datetime.now()
    
pre_save.connect(update_published_date, sender=Article)
"""