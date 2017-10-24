from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
import datetime
import MySQLdb
import abc, six
from neweb.views import *
class Food:
    counter=0
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.days=[]
        self.times=[]
        self.weekDayList = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.dayTimeList = ['Breakfast','Lunch','Snacks','Dinner']
        self.available="Not Available"
        Food.counter += 1
    def weeks(self, bitMask):
        bitMask -= 90000000
        weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for day in ['Friday','Thursday','Wednesday','Tuesday','Monday','Saturday','Sunday']:
            if bitMask%2==1:
                self.days.append(day)
                if day==weekdays[datetime.datetime.today().weekday()]:
                    self.available="Available"
            bitMask = bitMask/10
        return self.days
    def hours(self, bitMask):
        bitMask -= 90000
        for time in ['Dinner','Snacks','Lunch','Breakfast']:
            if bitMask%2==0:
                self.times.append(time)
            bitMask = bitMask/10
        return self.times
################################################################
class List:
    counter=0
    saturday=0
    sunday=0
    monday=0
    tuesday=0
    wednesday=0
    thursday=0
    friday=0
    allday=0
    def inc(self, day):
        if day=='Saturday':
            self.saturday+=1
        elif day=='Sunday':
            self.sunday+=1
        elif day=='Monday':
            self.monday+=1
        elif day=='Tuesday':
            self.tuesday+=1
        elif day=='Wednesday':
            self.wednesday+=1
        elif day=='Thursday':
            self.thursday+=1
        elif day=='Friday':
            self.friday+=1
        else:
            self.allday+=1
    def calc(self):
        conn=dbase()
        cursor=conn.getCursor()
        cursor.execute("select FoodName, FoodPrice, weekBitmask from FoodItem")
        row=cursor.fetchall()
        day=['Saturday',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday']
        count=0
        for div in [1000000,100000,10000,1000,100,10,1]:
            for i in row:
                if(count==0):
                    self.inc('all')
                if (((i[2]-90000000)/div)>=(1000000/div) and ((i[2]-90000000)/div)%2==1 ) or div==2:
                    self.inc(day[count])
            count+=1
################################################################
def getDetails(request, name):
    conn = dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from FoodItem where FoodName = '"+name+"'")
    row = cursor.fetchone()
    newFood = Food(row[1],row[2])
    days = newFood.weeks(row[3])
    times = newFood.hours(row[4])
    return render(request, "food/details.html", context = {'food':newFood})
###################################################################
def getEditForm(request, name):
    conn = dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from FoodItem where FoodName = '"+name+"'")
    row = cursor.fetchone()
    newFood = Food(row[1],row[2])
    days = newFood.weeks(row[3])
    times = newFood.hours(row[4])
    return render(request, "food/editForm.html", context = {'food':newFood})
###################################################################
def getList(request):
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor ()
    cursor.execute ("select FoodName, FoodPrice from FoodItem")
    if cursor.rowcount == 0:
        html = "{% extends 'home.html' %}\r\n{% block content%}\r\n<html><body>There is no Food</body></html>" 
    else:
        row = cursor.fetchall()
        html = "<html>"
	html += ' <table border = "1" > '
	html += "<tr> <td> <b> Food Name </b></td><td> <b>Food Price </b> </td> </tr>"
        for i in row:
            html += "<tr> <td>%s </td>  <td> %s</td> </tr>" % (i[0], i[1]) 
	html += "</table>"
        html += "</html>"
    return HttpResponse(html)
##########################################################################
def getWeeklyList(request, day):
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor ()
    name =""
    price=""
    cursor.execute ("select FoodName, FoodPrice, weekBitmask from FoodItem")
    if day=="Saturday":
        div=1000000;
    elif day=="Sunday":
        div=100000;
    elif day=="Monday":
        div=10000;
    elif day=="Tuesday":
        div=1000;
    elif day=="Wednesday":
        div=100;
    elif day=="Thursday":
        div=10;
    elif day=="Friday":
        div=1;
    else:
        div=2;
    if cursor.rowcount == 0:
        return render(request, "food/food.html", context = {'food':foodList}) 
    else:
        foodList=[]
        weekList=List()
        weekList.calc()
        row = cursor.fetchall()
        for i in row:
            if (((i[2]-90000000)/div)>=(1000000/div) and ((i[2]-90000000)/div)%2==1 ) or div==2:
                foodList.append(Food(i[0],i[1]))
	return render(request, "food/food.html", context = {'food':foodList, 'week':weekList}) 






    
