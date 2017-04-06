from django.db import models
from mma.models import Fight, Fighter, Event
from bookmakers.models import Bookmaker
from datetime import datetime

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

class BetType(models.Model):
    fighter_no = models.IntegerField(choices=((0,0),(1,1),(2,2)))
    bet_type_id = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    bet1_name = models.CharField(max_length=100, blank=True)
    bet2_name = models.CharField(max_length=100, blank=True)
    match_text = models.CharField(max_length=500, blank=True)
    value = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    
    def __unicode__(self):
        if self.fighter_no != 0:
            return str(self.fighter_no) + '_' + self.bet_type_id 
        else:
            return self.bet_type_id

class Bet(models.Model):
    fight = models.ForeignKey(Fight, blank=True, null=True, related_name='bet')
    event = models.ForeignKey(Event, blank=True, null=True)
    sportsbook = models.ForeignKey(Bookmaker)
    bet_type = models.ForeignKey(BetType, blank=True, null=True)
    bet1 = models.CharField(max_length=200)
    bet2 = models.CharField(max_length=200, blank=True, null=True)
    odds1 = models.IntegerField(blank=True, null=True)
    odds2 = models.IntegerField(blank=True, null=True)
    odds1_open = models.IntegerField(blank=True, null=True)
    odds2_open = models.IntegerField(blank=True, null=True)
    odds1_prev = models.IntegerField(blank=True, null=True)
    odds2_prev = models.IntegerField(blank=True, null=True)
    fighter1 = models.ForeignKey(Fighter, blank=True, null=True, related_name='bet_fighter1')
    fighter2 = models.ForeignKey(Fighter, blank=True, null=True, related_name='bet_fighter2')
    event_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(editable=False, default=now)
    
    def getBetProbability(self, bet_no):
        odds = Odds.objects.filter(bet=self)[0]
        current_odds = getattr(odds, 'odds'+str(bet_no))
        probability = (1/current_odds)*100
        return probability
    
    def __unicode__(self):
        if not self.bet_type:
            return str(self.fighter1) + '/' + str(self.fighter2)
        else:
            return str(self.fighter1) + '/' + str(self.fighter2) + ' - ' + self.bet_type.bet_type_id
        
class Odds(models.Model):
    bet = models.ForeignKey(Bet, related_name='odds')
    odds1 = models.IntegerField(blank=True, null=True)
    odds2 = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(editable=False, default=now)
    
    class Meta:
        ordering = ['-timestamp']
    
    
class OddsTable(models.Model):
    odds_table = models.TextField()