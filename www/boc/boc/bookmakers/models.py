from django.db import models
from tinymce.models import HTMLField
import random
from autoslug import AutoSlugField

# Create your models here.)
    
    
class Bookmaker(models.Model):
    name = models.CharField(max_length=50)
    api_id = models.IntegerField(blank=True, null=True)
    affiliate_url = models.CharField(max_length=100, blank=True, null=True)
    founded = models.CharField(max_length=10, blank=True)
    license = models.CharField(max_length=100, blank=True)
    known_for = models.CharField(max_length=100, blank=True)
    bonus = models.CharField(max_length=100, blank=True)
    countries_restricted =  models.CharField(max_length=200, blank=True)
    website =  models.CharField(max_length=100, blank=True)
    content = HTMLField(blank=True)
    slug = AutoSlugField(populate_from='name', editable=True)
    
    def __unicode__(self):
        return self.name
    
    def get_wide_banner(self):
        banners =  self.banner_set.filter(size='WI')
        if banners:
            return banners[0].banner_html
        else:
            return ''
        
    def get_square_banner(self):
        banners =  self.banner_set.filter(size='SQ')
        if banners:
            return banners[0].banner_html
        else:
            return ''
        
    def get_tall_banner(self):
        banners =  self.banner_set.filter(size='TA')
        if banners:
            return banners[0].banner_html
        else:
            return ''
        
    @models.permalink
    def get_absolute_url(self):
        return 'bookmakers:bookmaker', (), {'slug': self.slug}
        
    
    
class Banner(models.Model):
    
    WIDE = 'WI'
    TALL = 'TA'
    SQUARE = 'SQ'
    
    SIZE_CHOICES = (
        (WIDE, 'Wide'),
        (TALL, 'Tall'),
        (SQUARE, 'Square'))
    
    DESKTOP = 'DE'
    MOBILE = 'MO'
    
    PLATFORM_CHOICES = (
        (DESKTOP, 'Desktop'),
        (MOBILE, 'Mobile'))
    
    bookmaker = models.ForeignKey(Bookmaker)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    banner_html = HTMLField()
    
    def __unicode__(self):
        return '%s - %s'% (self.bookmaker.name,  self.size)
    
    
    @staticmethod
    def get_random_banner(size, platform):
        banners =  Banner.objects.filter(size=size, platform=platform)
        return random.choice(banners)

class BookmakerHead(models.Model):
    content = HTMLField(blank=True)
    def __unicode__(self):
        return self.content