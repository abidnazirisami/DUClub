# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.core.mail import EmailMessage
import MySQLdb
import abc, six
from django.shortcuts import render
from members.views import *
# Create your views here.

def mailHome(request):
    memberList=getMembers('')
    membersJSON = {}
    for member in memberList:
        membersJSON[member.name]=0
    return render(request, "mail/mailHome.html",context= {'members':membersJSON})
###################################################################3
def sendMail(request):
   subject = request.POST.get('subject', None)
   body = request.POST.get('message', None)
   email = EmailMessage(subject, body, to=["raidanahian@gmail.com","abidnazirisami@gmail.com","sdp02342017@gmail.com"])
   email.send()
   return render(request, "mail/sent.html")