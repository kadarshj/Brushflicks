"""brushflicks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from account import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^create/$', views.creativetype, name='creativetype'),

    url(r'^brushflick/addart$', views.art_share, name='art_share'),
    url(r'^liked/(?P<art_post_id>[0-9]+)/art_liked/(?P<user_id>[0-9]+)/$', views.art_liked, name='art_liked'),
    url(r'^flagged/(?P<art_post_id>[0-9]+)/art_flagged/(?P<user_id>[0-9]+)/$', views.art_flagged, name='art_flagged'),

    url(r'^brushflick/hire$', views.hire, name='hire'),
    url(r'^brushflick/hire/post$', views.hirehome, name='hirehome'),
    url(r'^brushflick/hiredetail$', views.hiredetailreq, name='hiredetail'),
    url(r'^brushflick/emailsent$', views.emailsent, name='emailsent'),

    url(r'^brushflick/gethire$', views.gethire, name='gethire'),
    url(r'^brushflick/gethire/post$', views.gethirehome, name='gethirehome'),
    url(r'^brushflick/gethiredetail$', views.gethiredetailreq, name='gethiredetail'),
    url(r'^brushflick/emailsent$', views.emailtosent, name='emailtosent'),

    url(r'^brushflick/profile_update/$', views.profileupdate, name='profile_update'),

    url(r'^brushflick/painting_image_sample/$', views.postpainterimg, name='paintingimage'),
    url(r'^brushflick/musician_music_sample/$', views.postmusic, name='postmusic'),
    url(r'^brushflick/photography_image_sample/$', views.postphoto, name='postphoto'),
    url(r'^brushflick/band_music_sample/$', views.postbandmusic, name='postbandmusic'),
    url(r'^brushflick/blogger_sample/$', views.postblog, name='postblog'),

    url(r'^brushflick/profile/$', views.profiledetails, name='profiledetails'),

    url(r'^brushflick/saved_card/$', views.artsavedcard, name='savedcard'),
    url(r'^brushflick/saved_card_delete/$', views.saveddelete, name='saveddelete'),

    url(r'^brushflick/sell_art$', views.sellartshare, name='sellartshare'),
    url(r'^brushflick/product_image_album/$', views.PostProductAlbum, name='SellProductAlbum'),
    url(r'^brushflick/Buy/art$', views.sellhome, name='sellhome'),
    url(r'^brushflick/buy/art/details$', views.sellartdetail, name='sellartdetail'),
    url(r'^brushflick/delivery_details/$', views.kart, name='kart'),
    url(r'^brushflick/payment/$', views.payment, name='payment'),
    url(r'^brushflick/success/$', views.success, name='success'),
    url(r'^brushflick/failure/$', views.failure, name='failure'),

    url(r'^brushflick/contact/$', views.contact, name='contact'),
    url(r'^brushflick/Symbol/Info/$', views.symbol, name='symbol'),


    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--

    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
