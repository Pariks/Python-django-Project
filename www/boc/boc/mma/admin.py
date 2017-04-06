from django.contrib import admin
from django.conf.urls import patterns, url
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from mma.models import Sport, Promotion, Event, Fighter, WeightClass, Fight

# Register your models here.

class FightAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_filter = ['event', 'api_id']
    
    list_display = ('event', 'order', 'weight_class', 'is_cancelled', 'fighter1', 'fighter2', 'fight_type', 'fighter_winner','method_of_victory_1',  'method_of_victory_2', 'round', 'duration')
    raw_id_fields = ('event', 'fighter1', 'fighter2', 'fighter_winner')

    def get_urls(self):
        
        urls = super(FightAdmin, self).get_urls()
        
        my_urls = patterns('',
            url(r'^pull_feed/$', self.admin_site.admin_view(self.pull_feed)),
        )
        return my_urls + urls

    def pull_feed(self, request):
            
        if request.method == 'POST':
            call_command('getmmadata')
            
        opts = self.model._meta
        url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name), current_app=self.admin_site.name)
        
        return HttpResponseRedirect(url)

class FighterAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name","date")}

admin.site.register(Sport)
admin.site.register(Promotion)
admin.site.register(Event, EventAdmin)
admin.site.register(Fighter, FighterAdmin)
admin.site.register(WeightClass)
admin.site.register(Fight, FightAdmin)