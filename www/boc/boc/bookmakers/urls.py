from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'bookmakers.views.index', name='index'),
url(r'^(?P<slug>[^\.]+)/$', 'bookmakers.views.bookmaker', name='bookmaker'),
)
