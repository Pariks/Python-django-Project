import re
from urllib2 import urlopen
from mma.models import Event, Fighter, Fight
from odds.models import BetType, Bet, Odds
from bookmakers.models import Bookmaker
import unicodedata 
import json
import datetime
from odds.views import update_odds_table
from decimal import *

class OddsFeed(object):
    
    def getObject(self, field, api_id):
        
        object_found = None
        
        if field == 'event':
            event_filter = Event.objects.filter(api_id=api_id)
            if event_filter.exists():
                object_found = event_filter[0]
                        
        elif field == 'fight':
            fight_filter = Fight.objects.filter(api_id=api_id)
            if fight_filter.exists():
                object_found = fight_filter[0]
        
        elif field == 'fighter1':
            fighter1_filter = Fighter.objects.filter(api_id=api_id)
            if fighter1_filter.exists():
                object_found = fighter1_filter[0]
                    
        elif field == 'fighter2':
            fighter2_filter = Fighter.objects.filter(api_id=api_id)
            if fighter2_filter.exists():
                object_found = fighter2_filter[0]
        
        return object_found
    
    def findOrCreateBetType(self, bet_type_api):
        bet_type = None
        if bet_type_api:
            bet_type_filter = BetType.objects.filter(pk=bet_type_api['id'])
            if bet_type_filter.exists():
                bet_type = bet_type_filter[0]
            else:
                bet_type = BetType(pk=bet_type_api['id'], 
                                   fighter_no=bet_type_api['fighter_no'],
                                   bet_type_id=bet_type_api['bet_type_id'],
                                   category=bet_type_api['category'],
                                   bet1_name=bet_type_api['bet1_name'],
                                   bet2_name=bet_type_api['bet2_name'],
                                   match_text=bet_type_api['match_text'],
                                   value=bet_type_api['value'])
                bet_type.save()
            
        return bet_type
    
    
    def getOdds(self):
        
        #Pull feed
        url = "http://139.162.152.182/api/bets/"
        
        client = urlopen(url)
        data = client.read()
        client.close()
        bets = json.loads(data)
        
        print 'got feed'
        bet_update_fields = ['bet1', 'bet2', 'bet_type', 'odds1', 'odds2', 'event', 'fight', 'fighter1', 'fighter2', 'odds1_open', 'odds2_open', 'odds1_prev', 'odds2_prev' , 'event_date']
        
        
        for bet in bets:
            #check if bet already in db
            bet_filter = Bet.objects.filter(pk=bet['id'])
            
            if bet_filter.exists():
                
                bet_db = bet_filter[0]
                
                #if yes, check if odds are different
                if (bet['odds1'] and bet_db.odds1 != int(bet['odds1'])) or(bet['odds2'] and bet_db.odds2 != int(bet['odds2'])):
                    odds = Odds(bet=bet_db, odds1=bet['odds1'], odds2=bet['odds2'])
                    odds.save()
                    #if yes, than add to odds row
               
                change_flag = False
                #update fields
                for field in bet_update_fields:
                    value = getattr(bet_db, field)
                    api_value =  bet[field]
                    
                    if type(value) is datetime.date:
                        value = value.strftime('%Y-%m-%d')
                        if value != api_value:
                            setattr(bet_db, field, api_value)
                    
                    elif 'odds' in field and bet[field]:
                        api_value = Decimal(api_value)
                        if value != api_value:
                            setattr(bet_db, field, api_value)
                        
                    elif field == 'event' or field == 'fight' or field == 'fighter1' or field == 'fighter2':
                        if bet[field]:
                            print bet[field]
                            object_found = self.getObject(field, bet[field])
                            if object_found:
                                api_value = object_found
                                if value != api_value:
                                    setattr(bet_db, field, api_value)
                   
                    elif field == 'bet_type':
                        api_value = self.findOrCreateBetType(bet['bet_type']) 
                        if value != api_value:
                            setattr(bet_db, field, api_value)
                
                    bet_db.save()
                    
            else:
                
                new_bet = Bet(pk=bet['id'])
                
                #find sportsbook
                sportsbook_filter = Bookmaker.objects.filter(api_id=bet['sportsbook']['id'])
                if sportsbook_filter.exists():
                    new_bet.sportsbook = sportsbook_filter[0]
                
                #set all fields
                missing_object = False
                for field in bet_update_fields:
                    
                    if type(bet[field]) is datetime.date:
                        value = value.strftime('%Y-%m-%d')
                        
                    if  field == 'fight' or field == 'fight' or field == 'fighter1' or field == 'fighter2':
                        if bet[field]:
                            object_found = self.getObject(field, bet[field])
                            if object_found:
                                setattr(new_bet, field, object_found)
                            else:
                                missing_object = True
                    elif field == 'event':
                        pass
                    
                    elif field == 'bet_type':
                        new_bet.bet_type = self.findOrCreateBetType(bet['bet_type'])
                    
                    else:
                        setattr(new_bet, field, bet[field])
                        
                if not missing_object:
                    new_bet.save()
                    odds = Odds(bet=new_bet, odds1=bet['odds1'], odds2=bet['odds2'])
                    
                    odds.save()
        
        
 
if __name__ == '__main__':
    import django
    django.setup()
    
    update_odds_table()
    oddsFeed = OddsFeed()
    oddsFeed.getOdds()
    