from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'testimonial.views.index', name='index'),
)
