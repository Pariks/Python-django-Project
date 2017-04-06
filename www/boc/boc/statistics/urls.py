from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'statistics.views.index', name='index'),
)
