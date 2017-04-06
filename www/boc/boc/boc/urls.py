from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from boc import views
from django.views.generic import TemplateView
from django.contrib.flatpages import views
from django.contrib.sitemaps.views import sitemap
from boc.sitemap import *
from django.contrib.sitemaps import FlatPageSitemap 

sitemaps = { 
            'main': MainSitemap,
            'odds_main':OddsMainSitemap,
            'flatpages': FlatPageSitemap, 
            'event_odds' : EventOddsSitemap,
            'event_fights' : EventFightsSitemap,
            'articles' : ArticleSitemap,
            'bookmakers' : BookmakerSitemap,
            'predictions' : PredictionSitemap
             }

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'boc.views.home', name='home'),
    url(r'^login/', 'boc.views.login', name='login'),
    #url(r'^settings/', 'boc.views.settings', name='settings'),
    #url(r'^loginvalidation/', views.loginvalidation, name='loginvalidation'),
    
    url(r'^join/', 'boc.views.join', name='join'),
    
    #url(r'^joinvalidation/', views.joinvalidation, name='joinvalidation'),
    url(r'^logout/', 'boc.views.logout', name='logout'),
    #url(r'^joinlogin/', views.joinlogin, name='joinlogin'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^odds/', include('odds.urls', namespace='odds')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^events/', include('mma.urls', namespace='mma')),
    url(r'^investing/', include('investor.urls', namespace='investor')),
    url(r'^predictions/', include('predictions.urls', namespace='predictions')),
    url(r'^bookmakers/', include('bookmakers.urls', namespace='bookmakers')),
    url(r'^testimonials/', include('testimonial.urls', namespace='testimonial')),
    url(r'^statistics/', include('statistics.urls', namespace='statistics')),
    url(r'^fantasy-mma/', include('fantasy.urls', namespace='fantasy')),
    url(r'^user-profile/', include('userprofile.urls', namespace='userprofile')),
    url(r'^consulting/', include('consulting.urls', namespace='consulting')),
    url(r'^login/', 'boc.views.login', name='login'),
    
    (r'^ckeditor/', include('ckeditor.urls')),
    
    url(r'^about/$', 'boc.views.about', name='about'),
    url(r'^about/the-fund/$', 'boc.views.about_fund', name='about_fund'),
    url(r'^about/advisory-board/$', 'boc.views.advisory_board', name='advisory_board'),

    url(r'^contact/$', 'boc.views.contact', name='contact'),
#    url(r'^career/$', views.flatpage, {'url': '/career/'}, name='career'),
    url(r'^career/$', 'boc.views.career', name='career'),
    url(r'^betting-guide/$', 'boc.views.betting_guide', name='betting_guide'),
    url(r'^learn/$', 'boc.views.learn', name='learn'),
    url(r'^learn/roi/$', 'boc.views.roi', name='roi'),
    url(r'^learn/become-a-student/$', 'boc.views.become_a_student', name='become_a_student'),
    url(r'^refer/$', views.flatpage, {'url': '/refer/'}, name='refer'),
    url(r'^affiliates/$', views.flatpage, {'url': '/affiliates/'}, name='affiliates'),
    url(r'^legal/$', 'boc.views.legal', name='legal'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^refer/$', views.flatpage, {'url': '/refer/'}, name='refer'),
    
    (r'^comments/', include('django_comments.urls')),
    
    url(r"^payments/", include("payments.urls")),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    
    url(r'^chat/', include('chat.urls', namespace="chat")),    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


