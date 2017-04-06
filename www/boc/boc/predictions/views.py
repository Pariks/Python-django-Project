from django.shortcuts import render
from predictions.models import Prediction, PredictionArticle
import datetime
from django.http import Http404
from django.conf import settings

def index(request):
    past_predictions = PredictionArticle.objects.filter(open=True).order_by('-timestamp')
    upcoming_predictions =  PredictionArticle.objects.filter(open=False).order_by('timestamp')
    #c ={'past_predictions': past_predictions}
    c ={'past_predictions': past_predictions, 'upcoming_predictions': upcoming_predictions}
    return render(request, 'predictions/predictions.html', c)


def predictionarticle(request, slug):
    prediction_article = PredictionArticle.objects.get(slug=slug)
    
    if not prediction_article:
        raise Http404
   
    events = prediction_article.get_events()
    
    c = {'prediction_article':prediction_article, 'events': events}
    return render(request, 'predictions/eventpredictions.html', c)