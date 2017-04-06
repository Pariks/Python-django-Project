from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'predictions.views.index', name='index'),
url(r'^(?P<slug>[^\.]+)/$', 'predictions.views.predictionarticle', name='predictionarticle'),
)
