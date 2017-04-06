from django.core.management import call_command
from odds.views import update_odds_table

def pull_mma_feed():
    call_command('getmmadata')
    
def pull_odds_feed():
    try:
        call_command('getodds')
        print 'get odds success'
    except:
        print 'get odds failed'
    
    try:
        update_odds_table()
        print 'update odds table success'
    except:
        print 'update odds table failed'  
    

