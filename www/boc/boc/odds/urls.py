from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'odds.views.index', name='index'),
url(r'^line-history/(?P<bet_id>\d+)/$', 'odds.views.line_history', name='line_history'),
)
