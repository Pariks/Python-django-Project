from django.core.management.base import BaseCommand
from odds.management.commands._oddsfeed import OddsFeed
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Match Bets'
    
    def handle(self, *args, **options):
        
        #initialize Odds parser
        oddsFeed = OddsFeed()
        oddsFeed.getOdds()