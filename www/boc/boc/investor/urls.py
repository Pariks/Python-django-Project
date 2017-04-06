from django.conf.urls import patterns, url
from investor.views import CountryChainedView

urlpatterns = patterns('',
    url(r'^$', 'investor.views.index', name='index'),
    url(r'^switch/$', 'investor.views.switch', name='switch'),
    url(r'^success/$', 'investor.views.success', name='success'),
    url(r'^fail/$', 'investor.views.failure', name='failure'),
    url(r'^ajax/custom-chained-view-url/$', CountryChainedView.as_view(), name='ajax_chained_country'),
)
