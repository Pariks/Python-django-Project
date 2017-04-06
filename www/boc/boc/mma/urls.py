from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'mma.views.index', name='index'),
    url(r'^upcoming/$', 'mma.views.upcoming_events', name='upcoming_events'),
    url(r'^past/$', 'mma.views.past_events', name='past_events'),
    url(r'^(?P<slug>[^\.]+)/fights/$', 'mma.views.event_fights', name='event_fights'),
    url(r'^(?P<slug>[^\.]+)/odds/$', 'mma.views.event_odds', name='event_odds')
)
