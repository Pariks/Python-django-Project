import re
from urllib2 import urlopen
from mma.models import Sport, Promotion, Event, Fighter, Fight, WeightClass 
import unicodedata 
import json
import datetime

class MMADataFeed(object):
    
    def updateData(self):
        
        #Pull feed
        url = "http://139.162.152.182/api/events/"
        
        client = urlopen(url)
        data = client.read()
        client.close()
        events = json.loads(data)
        
        event_update_fields = ['name', 'date', 'venue', 'city', 'broadcast']
        fight_update_fields = ['order', 'is_cancelled', 'is_championship', 'fight_type', 'method_of_victory_1', 'method_of_victory_2', 'round', 'duration']
     
        mma_sport = Sport.objects.get(name='MMA')
        
        for event in events:
            
            event_filter = Event.objects.filter(api_id=event['id'])
            event_db = None
            change_flag = False
            mma_sport = Sport.objects.get(name='MMA')
            if event_filter.exists():
                event_db = event_filter[0]
                for field in event_update_fields:
                    value = getattr(event_db, field)
                    if type(value) is datetime.date:
                        value = value.strftime('%Y-%m-%d')
                    
                    if value != event[field]:
                        setattr(event_db, field, event[field])
                        change_flag = True
                if change_flag:
                    event_db.save()
                
            else:
                promotion_filter = Promotion.objects.filter(api_id=event['promotion']['id'])
                if promotion_filter.exists():
                    promotion = promotion_filter[0]
                    event_date = datetime.datetime.strptime(event['date'], '%Y-%m-%d') 
                    event_db = Event(name=event['name'],
                                 date=event_date,
                                 venue=event['venue'],
                                 city=event['city'],
                                 broadcast=event['broadcast'],
                                 sport=mma_sport,
                                 promotion=promotion,
                                 api_id=event['id'])
                    
                    event_db.save()
                    
            if event_db:
                
                for fight in event['fights']:
                    fight_filter = Fight.objects.filter(api_id=fight['id'])
                    
                    if fight_filter.exists():
                        fight_db = fight_filter[0]
                        
                        #update text fields
                        for field in fight_update_fields:
                            value = getattr(fight_db, field)
                            if value != fight[field]:
                                setattr(fight_db, field, fight[field])
                                change_flag = True
                           
                        #fighter winner
                        if fight['fighter_winner']:
                            fighter_winner_filter = Fighter.objects.filter(api_id=fight['fighter_winner'])
                            if fighter_winner_filter.exists():
                                if fighter_winner_filter[0] != fight_db.fighter_winner:
                                    fight_db.fighter_winner = fighter_winner_filter[0]
                                    change_flag = True
                        
                        #weight class
                        if fight['weight_class']:
                            #check if weight class in db
                            weight_class_filter = WeightClass.objects.filter(api_id=fight['weight_class']['id'])
                            if weight_class_filter.exists():
                                #check if current weight does not match weight class, update if diff
                                if weight_class_filter[0] != fight_db.weight_class:
                                    fight_db.weight_class = weight_class_filter[0]
                                    change_flag = True
                            
                            #if no weightclass
                            else:
                                new_weight_class = WeightClass(sport=mma_sport, weight_class=fight['weight_class']['weight_class'], api_id=fight['weight_class']['id'], weight=fight['weight_class']['weight'] )
                                new_weight_class.save()
                                fight_db.weight_class = new_weight_class
                                change_flag = True
                                
                                
                        if change_flag:
                            fight_db.save()
                        
                    else:
                        #find or create fighter1
                        fighter1_filter = Fighter.objects.filter(api_id=fight['fighter1']['id'])
                        if fighter1_filter.exists():
                            fighter1 = fighter1_filter[0]
                        else:
                            fighter1 = Fighter(first_name=fight['fighter1']['first_name'], last_name=fight['fighter1']['last_name'], api_id=fight['fighter1']['id'])
                            fighter1.save()
                            
                        #find or create fighter2
                        fighter2_filter = Fighter.objects.filter(api_id=fight['fighter2']['id'])
                        if fighter2_filter.exists():
                            fighter2 = fighter2_filter[0]
                        else:
                            fighter2 = Fighter(first_name=fight['fighter2']['first_name'], last_name=fight['fighter2']['last_name'], api_id=fight['fighter2']['id'])
                            fighter2.save()
                        
                        
                        new_fight = Fight(fighter1=fighter1, fighter2=fighter2, event=event_db, api_id=fight['id'])
                        
                        #find or create weightclass
                        if fight['weight_class']:
                            weight_class_filter = WeightClass.objects.filter(api_id=fight['weight_class']['id'])
                            if weight_class_filter.exists():
                                weight_class = weight_class_filter[0]
                            else:
                                weight_class = WeightClass(sport=mma_sport, weight_class=fight['weight_class']['weight_class'], api_id=fight['weight_class']['id'], weight=fight['weight_class']['weight'] )
                                weight_class.save()
                                
                            setattr(new_fight, 'weight_class', weight_class)
                                
                        #create fight
                        
                        for field in fight_update_fields:
                            setattr(new_fight, field, fight[field])
                            
                        new_fight.save()
            
 
if __name__ == '__main__':
    import django
    django.setup()
    
    mmaDataFeed = MMADataFeed()
    mmaDataFeed.updateData()