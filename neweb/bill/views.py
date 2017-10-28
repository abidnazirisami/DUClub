# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from members.views import *
from lounge.views import *
import MySQLdb
import abc, six
import datetime
from dateutil.tz import tzlocal


###############################################################################################

def billForm(request):
    memberList=getMembers('')
    membersJSON = {}
    for member in memberList:
        membersJSON[member.name]=0
    loungeList = getLoungeList()
    loungeJSON = {}
    for lounge in loungeList:
        loungeJSON[lounge.name] = 0
    today={'year':datetime.datetime.now(tzlocal()).year, 'month':datetime.datetime.now(tzlocal()).month, 'day':datetime.datetime.now(tzlocal()).day}
    return render(request, "bill/billForm.html", context ={'warning':"",'members':membersJSON, 'today': today, 'lounges': loungeJSON})

###############################################################################################

def submitBill(request):
    name = request.POST.get('member_name',None)
    date = request.POST.get('date', None)
    if not name:
        return render(request, "bill/billForm.html", context={'warning':"Please insert the name of the member"})
    return render(request, "bill/billCreated.html", context = {'name': name, 'date': date})

###############################################################################################
