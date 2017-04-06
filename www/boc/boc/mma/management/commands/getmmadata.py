from django.core.management.base import BaseCommand
from mma.management.commands._mmadatafeed import MMADataFeed
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Match Bets'
    
    def handle(self, *args, **options):
        
        #initialize Odds parser
        mmaDataFeed = MMADataFeed()
        mmaDataFeed.updateData()