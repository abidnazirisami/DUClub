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
    cost = 0
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
    def calculatePrice(self):
        conn = Singleton.dbase()
        cursor = conn.getCursor ()
        args = [self.name,]
        cursor.callproc ("searchFoodWithName", args)
        row = cursor.fetchone()
        self.cost = (int)(self.quantity)*(int)(row[2])
        self.id = row[0]
        return self.cost

###############################################################################################

def billForm(request):
    memberList=getMembers('')
    membersJSON = {}
    for member in memberList:
        key=member.name
        key+=str(' [ID: ')
        key+=str(member.id)
        key+=str(']')
        membersJSON[key]=0
    loungeList = getLoungeList()
    loungeJSON = {}
    for lounge in loungeList:
        loungeJSON[lounge.name] = 0
    now = datetime.datetime.now()
    
    today={'year':now.year, 'month':now.month, 'day':now.day}
    foodDict=getFoodList('All')
    return render(request, "bill/billForm.html", context ={'warning':"",'members':membersJSON, 'today': today, 'lounges': loungeJSON, 'foods': foodDict['food']})

###############################################################################################

def submitBill(request):
    name = request.POST.get('member_name',None)
    date = request.POST.get('date', None)
    lounge = request.POST.get('lounge_name', None)
    foodList = request.POST.getlist('foodname')
    quantity = request.POST.getlist('itemNum')
    splitname = name.split(" [")
    name=splitname[0]
    items = []
    index=0
    cost=0
    discount = 0
    conn = Singleton.dbase()
    cursor = conn.getCursor()
    cursor.execute ("select MemberID from Accounts where MemberName like '%%%s%%'" %name)
    row = cursor.fetchone()
    memberid = row[0]
    cursor.execute ("select LoungeID from Lounge where LoungeName like '%%%s%%'" %lounge)
    row = cursor.fetchone()
    loungeid = row[0]
    args = [loungeid,memberid,date,discount,cost,]
    cursor.callproc("addNewBill", args)
    cursor.execute("select last_insert_id()");
    row = cursor.fetchone()
    billID = row[0]
    for food in foodList:
        items.append(Item(food, quantity[index]))
        cost=cost+(int)(items[index].calculatePrice())
        args = [items[index].id,billID,quantity[index],]
        cursor.callproc("foodToBill", args)
        index+=1
    args = [cost,billID,]
    cursor.callproc("updateTotal",args)
    conn.commit()
    return render(request, "bill/billCreated.html", context = {'name': name, 'date': date, 'food': items,'cost': cost})

###############################################################################################

