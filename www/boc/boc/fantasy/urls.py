from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'fantasy.views.index', name='index'),
)
