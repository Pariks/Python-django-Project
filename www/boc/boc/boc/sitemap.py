from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from bookmakers.models import Bookmaker
from mma.models import Event
from news.models import Article
from predictions.models import PredictionArticle


#statics pages


class OddsMainSitemap(Sitemap):
    priority = 0.9
    changefreq = 'always'

    def items(self):
        return ['odds:index']

    def location(self, item):
        return reverse(item)


class MainSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['home', 'mma:index', 'mma:past_events', 'mma:upcoming_events', 'news:index', 'predictions:index','investor:index', 'fantasy:index', 'chat:index']

    def location(self, item):
        return reverse(item)


class BookmakerSitemap(Sitemap):
    priority = 0.5
    
    def items(self):
        return Bookmaker.objects.all()
    
class EventOddsSitemap(Sitemap):
    priority = 0.7
    
    def items(self):
        return Event.objects.all()

    def location(self, obj):
        return obj.get_odds_url()   
    
class EventFightsSitemap(Sitemap):
    priority = 0.6
    
    def items(self):
        return Event.objects.all()

    def location(self, obj):
        return obj.get_odds_url()
    
class PredictionSitemap(Sitemap): 
    priority = 0.7
    
    def items(self):
        return PredictionArticle.objects.all()

    def lastmod(self, obj):
        return obj.timestamp
    
class ArticleSitemap(Sitemap): 
    priority = 0.7
    
    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.date_updated