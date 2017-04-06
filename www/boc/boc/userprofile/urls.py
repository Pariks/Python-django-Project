from django.conf.urls import patterns, url

urlpatterns = patterns('',
url(r'^$', 'userprofile.views.index', name='index'),
url(r'^phone-number/$', 'userprofile.views.phone_number', name='phone_number'),
url(r'^avatar/$', 'userprofile.views.avatar_update', name='avatar_update'),
url(r'^follow/(?P<username>[^\.]+)/$', 'userprofile.views.follow_user', name='follow_user'),
url(r'^(?P<username>[^\.]+)/$', 'userprofile.views.profile_display', name='profile_display'),
)
