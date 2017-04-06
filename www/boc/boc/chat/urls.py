from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'chat.views.index', name='index'),
    url(r'^auth/$', 'chat.views.auth', name='auth'),
    url(r'^message/$', 'chat.views.message', name='message'),
     url(r'^sound/$', 'chat.views.chat_sound', name='sound')
)
   
