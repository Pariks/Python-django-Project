from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'consulting.views.index', name='index'),
)  

