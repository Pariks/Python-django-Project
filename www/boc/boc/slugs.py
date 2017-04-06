
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boc.settings")

    from predictions.models import PredictionArticle
    from bookmakers.models import Bookmaker
    from mma.models import Event
    from django.conf import settings


    articles = PredictionArticle.objects.all()
    
    for article in articles:
        article.save()
        
    bookmakers = Bookmaker.objects.all()
    
    for bookmaker in bookmakers:
        bookmaker.save()
        
    events = Event.objects.all()
    
    for event in events:
        event.save()