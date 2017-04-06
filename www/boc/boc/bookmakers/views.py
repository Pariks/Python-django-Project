from django.shortcuts import render
from bookmakers.models import Bookmaker, BookmakerHead

def index(request):
    bookmakers = Bookmaker.objects.all()
    bookmakersheads = BookmakerHead.objects.all()
    c ={'bookmakers':bookmakers, 'bookmakersheads': bookmakersheads}
    return render(request, 'bookmakers/bookmakers.html', c)

def bookmaker(request, slug):
    bookmaker = Bookmaker.objects.get(slug=slug)
    c = {'bookmaker': bookmaker}
    return render(request, 'bookmakers/bookmaker.html', c)
    
    