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
]