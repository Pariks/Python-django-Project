from django.shortcuts import render
from mma.models import Event, Fight
from odds.views import get_odds
from datetime import datetime
from django.http import Http404
import json

# Create your views here.
def index(request):
    upcoming_events = Event.objects.filter(date__gte=datetime.now()).order_by('date')[:4]
    recent_events = Event.objects.filter(date__lt=datetime.now()).order_by('-date')[:4]
    c = {'upcoming_events': upcoming_events, 'recent_events':recent_events}
    
    return render(request, 'mma/events.html', c)

def upcoming_events(request):
    events = Event.objects.filter(date__gte=datetime.now()).order_by('date')
    c = {'events': events, 'title': 'Upcoming'}
    
    return render(request, 'mma/upcoming_past_events.html', c)

def past_events(request):
    events = Event.objects.filter(date__lt=datetime.now()).order_by('-date')
    c = {'events': events, 'title': 'Past'}
    
    return render(request, 'mma/upcoming_past_events.html', c)

def event_fights(request, slug):
    event = Event.objects.get(slug=slug)
    page = 'Fights'
    
    if not event:
        raise Http404
    
    fights = Fight.objects.filter(event=event, is_cancelled=False).order_by('order')
   
    c = {'event':event, 'fights':fights, 'page':page}
    return render(request, 'mma/event.html', c)


def event_odds(request, slug):
    event = Event.objects.get(slug=slug)
    page = 'Odds'
    
    if not event:
        raise Http404
    
    fights = Fight.objects.filter(event=event, is_cancelled=False).order_by('order')
    
    event_odds = get_odds([event])
    if len(event_odds) > 0:
        
        event_odds = event_odds[0]['events'][0]
    
   
    c = {'event':event, 'fights':fights, 'page': page, 'event_odds': json.dumps(event_odds)}
    return render(request, 'mma/event.html', c)