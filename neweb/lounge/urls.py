from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', loungeHome),
    url(r'^search/$', search),
    url(r'^addLounge/$', addLounge),
    url(r'^loungeForm/$', addLng),
    url(r'^deleteLounge/$', deleteLounge),
    url(r'^deleteLng/(.{1,30})/$', deleteLng),
    url(r'^updateLounge/$', updateLounge),
    url(r'^details/(.{1,30})', getDetails),
    url(r'^add/$', addLoungePage),
    url(r'^delete/(.{1,30})/$', deleteLoungePage),
    url(r'^update/(.{1,30})/$', updateLoungePage),
]
