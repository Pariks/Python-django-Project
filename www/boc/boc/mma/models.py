from django.db import models
import datetime
from autoslug import AutoSlugField

class Sport(models.Model):
    name = models.CharField(max_length=50)
    
    
    def __unicode__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField(max_length=50)
    sport = models.ForeignKey(Sport)
    api_id = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
  
def event_sluggify(instance):
    return  instance.name +' '+ instance.date.isoformat()

class Event(models.Model):
    
    name = models.CharField(max_length=100)
    date = models.DateField()
    venue = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=100, blank=True)
    sport = models.ForeignKey(Sport)
    promotion = models.ForeignKey(Promotion)
    broadcast = models.CharField(max_length=25, blank=True)
    poster = models.ImageField(upload_to='uploads/events', blank=True)
    api_id = models.IntegerField(blank=True, null=True)
    slug = AutoSlugField(populate_from=event_sluggify, editable=True)
    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
    
    @staticmethod
    def next_event():
        events = Event.objects.filter(date__gte=datetime.date.today()).order_by('date')
        if events:
            return events[0]
        else:
            return None 
    
    @staticmethod
    def last_event():
        events = Event.objects.filter(date__lte=datetime.date.today()).order_by('-date')
        if events:
            return events[0]
        else:
            return None


    @models.permalink
    def get_fights_url(self):
        return 'mma:event_fights', (), {'slug': self.slug}
    
    
    @models.permalink
    def get_odds_url(self):
        return 'mma:event_odds', (), {'slug': self.slug}

    

class Fighter(models.Model):
    
    #names
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    api_id = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']

class WeightClass(models.Model):
    weight_class = models.CharField(max_length=20, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    sport = models.ForeignKey(Sport, null=True, blank=True)
    api_id = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s (%s)"% (self.weight_class,  self.weight)
    

class Fight(models.Model):
    MAIN_EVENT = 'ME'
    CO_MAIN_EVENT = 'CO'
    MAIN_CARD = 'MC'
    PRELIM = 'PL'
    
    FIGHT_TYPE_CHOICES = (
                   (MAIN_EVENT, 'Main Event'),
                   (CO_MAIN_EVENT, 'Co-Main Event'),
                   (MAIN_CARD, 'Main Card'),
                   (PRELIM, 'Preliminary Card'),
                   )
      
    event = models.ForeignKey(Event, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)
    weight_class = models.ForeignKey(WeightClass, null=True, blank=True)
    fighter1 = models.ForeignKey(Fighter, related_name='fighter1')
    fighter2 = models.ForeignKey(Fighter, related_name='fighter2')
    fight_type = models.CharField(max_length=2, choices=FIGHT_TYPE_CHOICES, blank=True)
    
    is_championship = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    fighter_winner = models.ForeignKey(Fighter, related_name='winner', blank=True, null=True)
    method_of_victory_1 = models.CharField(max_length=50, blank=True)
    method_of_victory_2 = models.CharField(max_length=50, blank=True)
    round = models.PositiveSmallIntegerField(null=True, blank=True)
    duration = models.CharField(max_length=5, blank=True)
    
    api_id = models.IntegerField(blank=True, null=True)
    
    def get_field_list(self):
        db_field_names = []
            
        for db_field in self._meta.fields:
            db_field_names.append(db_field.name)
            
        return db_field_names
    
    def fighter_loser(self):
        if self.fighter1 == self.fighter_winner:
            return self.fighter2
        else:
            return self.fighter1
    
    def get_result(self):
        if self.method_of_victory_1.lower() == 'decision':
            return "%s Round Decision (%s)"% (self.round, self.method_of_victory_2)
        else:
            return "%s (%s) at %s of Round %s"% (self.method_of_victory_1, self.method_of_victory_2, self.duration, self.round)
    
    
    class Meta:
        ordering = ['event']
    
    def __unicode__(self):
        return "%s: %s/%s"% (self.event, self.fighter1, self.fighter2)
    
    