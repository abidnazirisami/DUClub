# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from members.views import *
from lounge.views import *
from food.views import *
import MySQLdb
import abc, six
import datetime
from dateutil.tz import tzlocal
###############################################################################################
class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

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
    foodDict=getFoodList('All')
    return render(request, "bill/billForm.html", context ={'warning':"",'members':membersJSON, 'today': today, 'lounges': loungeJSON, 'foods': foodDict['food']})

###############################################################################################

def submitBill(request):
    name = request.POST.get('member_name',None)
    date = request.POST.get('date', None)
    foodList = request.POST.getlist('foodname')
    quantity = request.POST.getlist('itemNum')
    items = []
    index=0
    for food in foodList:
        items.append(Item(food, quantity[index]))
        index+=1
    if not name:
        return render(request, "bill/billForm.html", context={'warning':"Please insert the name of the member"})
    return render(request, "bill/billCreated.html", context = {'name': name, 'date': date, 'food': items})

###############################################################################################
