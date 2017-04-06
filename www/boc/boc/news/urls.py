from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'news.views.index', name='index'),
url(r'^comment_replies/(?P<slug>[^\.]+)/(?P<comment_id>[0-9]+)/$', 'news.views.comment_replies', name='comment_replies'),
url(r'^(?P<slug>[^\.]+)/$', 'news.views.article', name='article'),
url(r'^(?P<slug>[^\.]+)/comment$', 'news.views.comment', name='comment'),
)
