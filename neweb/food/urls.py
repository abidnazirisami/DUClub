from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^details/(.{1,30})', getDetails),
    url(r'^edit/(.{1,30})', getEditForm),
    url(r'^success/(.{1,30})', getEditResponse),
    url(r'^(.{0,30})$', getWeeklyList),
]
