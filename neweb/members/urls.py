from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    url(r'^$', memberHome),
    url(r'^search/$', search),
    url(r'^addMember/$', addMember),
    url(r'^memberForm/$', addMem),
    url(r'^deleteMember/$', deleteMemberPage),
    url(r'^delete/$', deleteMember),
    url(r'^updateMember/$', updateMemberPage),
    url(r'^update/$', updateMember),
    url(r'^deleteMem/$', deleteMem),
]
