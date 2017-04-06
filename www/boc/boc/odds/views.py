from django.shortcuts import render
from odds.models import Bet, BetType, Odds, OddsTable
from mma.models import Event, Fighter
import datetime
import json
import datetime
from django.core import serializers
from django.http import HttpResponse, Http404, JsonResponse

def get_odds(events):
    """
    [
        {
            name: eventname ...,
            date: ...,
            fights: [
                {
                    fighter1: fighter1...,
                    bets: {
                        straight:[
                            bettype
                            bet1: ''
                            bet2: ''
                        
                        ]
                        general props:[
                            {
                                bet1: 'Draw',
                                bet2: 'Not draw',
                                odds1: [
                                    {sportsbookname: 5dimes, odds: 150, odds_prev: 140},
                                    {sportsbookname: betdsi, odds: 150, odds_prev: 140},
                                ],
                                odds2: [
                                    {sportsbookname: 5dimes, odds: 150, odds_prev: 140},
                                    {sportsbookname: betdsi, odds: 150, odds_prev: 140},
                                ]
                            },
                            {
                                ....
                            }
                        ]
                        distance props:
                        fighter1 props:
                        fighter2 props:
                    }
                }
                
            ]
        }
    ]
    month:[
        event1:[
            fight1:
            fight2
            ]
            
    
    
    """
    
    bet_type_order = ['straight', 'draw', 'points', 
                      'over/under', 'distance', 'start round', 'end round',
                      'win method', 'win round', 'win minute',
                      'fastest winner', 'fight of the night', 'win method of the night']
    sportsbook_order = ['5Dimes', 'BetDSI', 'Bookmaker']
    
    bet_type_dict = {'straight': 'straight', 
                     'draw':'general props', 'points':'general props', 'fight of the night': 'general props', 'straight (no scorecards)': 'general props',
                     'over/under': 'distance props', 'distance': 'distance props', 'start round': 'distance props','end round': 'distance props',
                     'win method': 'fighter props', 'win round': 'fighter props', 'win minute':'fighter props', 'win method of the night': 'fighter props', 'fastest winner':'general props'
                    }
   
    
    dict = []
    last_month = None
    month_index = -1
    
    #loop through each event
    for event in events:
        current_month = datetime.date(event.date.year, event.date.month, 1)
        
        #get fights
        fights = event.fight_set.filter(is_cancelled=False)
        
        #loop through each fight
        for fight in fights:
            
            #check if fight has bets
            if fight.bet.exists():
                
                #check if current month in dictionary
                if current_month != last_month:
                    last_month = current_month
                    month_index = month_index + 1
                    month_dict = {'month': current_month.strftime("%B"), 'events':[]}
                    dict.append(month_dict)
                    
                events_array = dict[month_index]['events']
                
                #get events index
                event_index = -1
                i = 0
                while i < len(events_array):
                    if events_array[i]['id'] == event.id:
                        event_index = i
                    i = i+1
                    
                #add event into array 
                if event_index == -1:
                    event_dict = {'slug':event.get_odds_url(), 'id':event.id, 'name': event.name, 'date':event.date.strftime("%b %d, %Y"), 'fights': [], 'last_updated':None}
                    events_array.append(event_dict)
                    event_index = len(events_array) - 1
                    
                fight_array = events_array[event_index]['fights']
                
                #add fight into array
                fight_dict = {'fighter1':fight.fighter1.first_name+' '+fight.fighter1.last_name, 
                       'fighter1_last_name':fight.fighter1.last_name,     
                       'fighter2':fight.fighter2.first_name+' '+fight.fighter2.last_name,
                       'fighter2_last_name':fight.fighter2.last_name,     
                       'prop_count': 0,
                       'bets':{'straight':[], 'general props':[], 'distance props':[], 'fighter1 props':[], 'fighter2 props': []},
                       'order':fight.order}
                fight_array.append(fight_dict) 
                fight_index = len(fight_array)-1
                
                bets = fight.bet.all()
                
                #loop through each bet
                for bet in bets:
                    
                    if bet.bet_type:
                        
                        #determine which general category the bet belongs to
                        bet_type_category = bet_type_dict[bet.bet_type.category]
                        
                        #get bet1 name and bet2 name
                        if bet_type_category == 'straight':
                            bet1_name = fight_array[fight_index]['fighter1']
                            bet2_name = fight_array[fight_index]['fighter2'] 
                        
                        elif bet_type_category == 'fighter props':
                            if bet.bet_type.fighter_no == 1:
                                bet_type_category = 'fighter1 props'
                                bet1_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet1_name
                                bet2_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet2_name
                            elif bet.bet_type.fighter_no == 2:
                                bet_type_category = 'fighter2 props'
                                bet1_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet1_name
                                bet2_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet2_name
                        
                        else:
                            if bet.bet_type.category == 'straight (no scorecards)':
                                bet1_name = bet.bet1
                                bet2_name = bet.bet2
                            elif bet.bet_type.category == 'points':
                                if fight_array[fight_index]['bets']['straight'][0]['best_odds1'] < fight_array[fight_index]['bets']['straight'][0]['best_odds2']:
                                   
                                   
                                    if fight.fighter1.last_name in bet.bet1:
                                        bet1_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet1_name
                                        bet2_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet2_name
                                    else:
                                        bet2_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet1_name
                                        bet1_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet2_name
                                else:
                                    if fight.fighter1.last_name in bet.bet1:
                                        bet2_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet2_name
                                        bet1_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet1_name
                                    else:
                                        bet1_name = fight_array[fight_index]['fighter1_last_name']+' '+bet.bet_type.bet2_name
                                        bet2_name = fight_array[fight_index]['fighter2_last_name']+' '+bet.bet_type.bet1_name
                            elif bet.bet_type.category == 'fastest winner':
                                bet1_name = bet.bet1
                                bet2_name = bet.bet2
                            else:  
                                bet1_name = bet.bet_type.bet1_name
                                bet2_name = bet.bet_type.bet2_name
                            
                            
                        #check whether bet is in category
                        bet_index = -1
                        i = 0
                        
                        while i < len(fight_array[fight_index]['bets'][bet_type_category]):
                            if fight_array[fight_index]['bets'][bet_type_category][i]['bet_type_id'] == bet.bet_type.bet_type_id:
                                bet_index = i
                            i = i+1
                        
                        bet_array = fight_array[fight_index]['bets'][bet_type_category]
                        
                        if bet_index == -1:
                            #no? add bet into dicitonary
                            bet_dict = {
                                        'id': bet.id,
                                        'bet_type_id':bet.bet_type.bet_type_id,
                                       'bet_type_value': str(bet.bet_type.value),
                                       'bet1':bet1_name,
                                       'bet2':bet2_name,
                                       'best_odds1': str(bet.odds1), 
                                       'best_odds2': str(bet.odds2), 
                                       'odds':{}}
                            
                            bet_array.append(bet_dict)
                            bet_index = len(bet_array) - 1
                            
                            #update prop count
                            if bet.bet_type.category != 'straight':
                                fight_array[fight_index]['prop_count'] = fight_array[fight_index]['prop_count']+1
                                
                        odds1_arrow = 'remove'
                        if bet.odds1_prev:
                            if bet.odds1_prev > bet.odds1:
                                odds1_arrow = 'arrow_drop_down'
                            elif  bet.odds1_prev < bet.odds1:
                                odds1_arrow = 'arrow_drop_up'
                        
                        odds2_arrow = 'remove' 
                        if bet.odds2_prev: 
                            if bet.odds2_prev > bet.odds2:
                                odds2_arrow = 'arrow_drop_down'
                            elif  bet.odds2_prev < bet.odds2:
                                odds2_arrow = 'arrow_drop_up'
                        
                        
                        bet_array[bet_index]['odds'][bet.sportsbook.name] = {
                                                                            'id': bet.id,
                                                                             'odds1': str(bet.odds1), 
                                                                              'odds2': str(bet.odds2),
                                                                              'odds1_prev': str(bet.odds1_prev),
                                                                              'odds2_prev': str(bet.odds2_prev),
                                                                              'odds1_arrow': odds1_arrow,
                                                                              'odds2_arrow': odds2_arrow
                                                                              }
                        
                      
                        #update best odds
                        if  bet.odds1 > float(bet_array[bet_index]['best_odds1']):
                            bet_array[bet_index]['best_odds1'] = str(bet.odds1)
                       
                        if bet_array[bet_index]['best_odds2'] == 'None' or bet.odds2 > float(bet_array[bet_index]['best_odds2']):
                            bet_array[bet_index]['best_odds2'] = str(bet.odds2)
                        
                        #update last updated
                        if not events_array[event_index]['last_updated'] or bet.timestamp > events_array[event_index]['last_updated']:
                            events_array[event_index]['last_updated'] = bet.timestamp
                                  
    for month in dict:
        for event in month['events']:
            event['last_updated'] = event['last_updated'].strftime('%Y-%m-%dT%H:%M:%SZ')
            
    return dict

def line_history(request, bet_id):
    line_history = Odds.objects.filter(bet=bet_id).order_by('timestamp')
    line_history = serializers.serialize("json", line_history)
    return HttpResponse(line_history, content_type="application/json")


def index(request):
    
    """
    events = Event.objects.filter(date__gte=datetime.datetime.now()).order_by('date')
    odds = get_odds(events)
    c ={ 'months': json.dumps(odds) }
    return render(request, 'odds/odds.html', c)
    """
    odds_table = OddsTable.objects.get(pk=1)
    c ={ 'months': odds_table.odds_table }
    return render(request, 'odds/odds.html', c)
   


def update_odds_table():
    events = Event.objects.filter(date__gte=(datetime.datetime.now()-datetime.timedelta(hours=9))).order_by('date')
    odds = get_odds(events)
    odds_table = OddsTable.objects.get(pk=1)
    odds_table.odds_table = json.dumps(odds)
    odds_table.save()
