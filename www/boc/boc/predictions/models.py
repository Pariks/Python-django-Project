from django.db import models
from tinymce.models import HTMLField
import datetime
from autoslug import AutoSlugField
from django.utils import timezone

from mma.models import Fight, Sport, Event

# Create your models here.
class PredictionArticle(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/predictions', blank=True)
    content = HTMLField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)
    open = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='title', editable=True)
    
    def __unicode__(self):
        return "%s: %s"% (self.title, self.timestamp)
    
    
    def get_events(self):
        predictions = self.prediction_set.all()
        events = []
        for prediction in predictions:
            for fight in prediction.fight.all():
                if fight.event not in events:
                    events.append(fight.event)
                
        return events
            
    
    @staticmethod
    def next_prediction():
        prediction_articles = PredictionArticle.objects.filter(open=False).order_by('timestamp')
        if prediction_articles:
            return prediction_articles[:2]
        else:
            return None 
    
    @staticmethod
    def last_prediction():
        prediction_articles = PredictionArticle.objects.filter(open=True).order_by('-timestamp')
        if prediction_articles:
            return prediction_articles[:2]
        else:
            return None
    
    @property
    def get_record(self):
        return str(self.prediction.prediction_set.all.filter(result='Win').count()) +'-'+str(self.prediction.prediction_set.all.filter(result='Loss').count())
    
    @models.permalink
    def get_absolute_url(self):
        return 'predictions:predictionarticle', (), {'slug': self.slug}
    
    class Meta:
        ordering = ['-timestamp']
    
class Prediction(models.Model):
    STRAIGHT = 'ST'
    PARLAY = 'PA'
    PROP = 'PR'
    
    BET_TYPE_CHOICES = (
                   (STRAIGHT, 'Straight Bet'),
                   (PARLAY, 'Parlay'),
                   (PROP, 'Prop')
                   )
    
    WIN = 'Win'
    LOSS = 'Loss'
    PUSH = 'Push'
    PENDING = 'Pending'
    VOID = 'Void'
    
    RESULT_CHOICES = (
                      (WIN, 'Win'),
                      (LOSS, 'Loss'),
                      (PUSH, 'Push'),
                      (PENDING, 'Pending'),
                      (VOID, 'Void')
                      )
    
    fight = models.ManyToManyField(Fight, blank=True)
    sport = models.ManyToManyField(Sport)
    prediction_article = models.ForeignKey(PredictionArticle)
    order = models.IntegerField(blank=True, null=True)
    
    fighter1_odds = models.IntegerField(blank=True, null=True)
    fighter2_odds = models.IntegerField(blank=True, null=True)
    
    fighter1_percent =  models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fighter2_percent =  models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    bet_type = models.CharField(max_length=2, choices=BET_TYPE_CHOICES)
    prediction = HTMLField(blank=True, null=True)
    odds = models.CharField(max_length=20)
    risk = models.DecimalField(max_digits=20, decimal_places=2)
    win = models.DecimalField(max_digits=20, decimal_places=2)
    breakdown = HTMLField(blank=True, null=True)
    outcome = HTMLField(blank=True, null=True)
    result  = models.CharField(max_length=7, choices=RESULT_CHOICES, default=PENDING)
    
    
    class Meta:
        ordering = ['-prediction_article__timestamp', 'order']
        
    def __unicode__(self):
        return "%s: %s"% (self.prediction_article.title, self.bet_type)
    
    
   
    