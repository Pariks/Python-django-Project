from django.contrib import admin
from django.conf.urls import patterns, url
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from odds.models import BetType, Odds, Bet, OddsTable
from odds.views import update_odds_table

class BetAdmin(admin.ModelAdmin):
    list_display = ('fight', 'event',  'sportsbook', 'bet_type', 'bet1', 'bet2',  'fighter1', 'fighter2', 'event_date', 'timestamp')
    list_filter = ('sportsbook', 'bet_type')
    search_fields = ['fighter1__first_name', 'fighter2__first_name','fighter1__last_name', 'fighter2__last_name','bet1','bet2']
    raw_id_fields = ('fight', 'fighter1', 'fighter2')
    readonly_fields=('id',)    
    
    def get_urls(self):
        
        urls = super(BetAdmin, self).get_urls()
        
        my_urls = patterns('',
            url(r'^pull_odds_feed/$', self.admin_site.admin_view(self.pull_odds_feed)),
            url(r'^update_odds_table/$', self.admin_site.admin_view(self.update_odds_table)),
        )
        return my_urls + urls
    
    def pull_odds_feed(self, request):
            
        if request.method == 'POST':
            call_command('getodds')
            
        opts = self.model._meta
        url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name), current_app=self.admin_site.name)
        
        return HttpResponseRedirect(url)
    
    def update_odds_table(self, request):
            
        if request.method == 'POST':
            update_odds_table()
            
        opts = self.model._meta
        url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name), current_app=self.admin_site.name)
        
        return HttpResponseRedirect(url)

class OddsAdmin(admin.ModelAdmin):
    list_display = ('bet', 'odds1', 'odds2', 'timestamp')
    raw_id_fields = ('bet',)    
    search_fields = ['bet__fighter1__first_name', 'bet__fighter2__first_name', 'bet__fighter1__last_name', 'bet__fighter2__last_name', 'bet__bet_type__bet_type_id']

admin.site.register(BetType)
admin.site.register(Odds, OddsAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(OddsTable)