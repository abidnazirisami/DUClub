from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
import datetime
import MySQLdb
import abc, six
from neweb.views import *


#########################################################################
################################# F O O D ###############################
#########################################################################
class Food:
    weekDayList = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.days=[]
        self.times=[]
        self.dayTimeList = ['Breakfast','Lunch','Snacks','Dinner']
        self.available="Not Available"
#########################################################################      
    
    def getWeekdays(self, bitMask):
        bitMask -= 90000000
        weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for day in ['Friday','Thursday','Wednesday','Tuesday','Monday','Sunday','Saturday']:
            if bitMask%2==1:
                self.days.append(day)
                if day==weekdays[datetime.datetime.today().weekday()]:
                    self.available="Available"
            bitMask = bitMask/10
        self.days.reverse()
        return self.days
#########################################################################    
    def getHours(self, bitMask):
        bitMask -= 90000
        for time in ['Dinner','Snacks','Lunch','Breakfast']:
            if bitMask%2==1:
                self.times.append(time)
            bitMask = bitMask/10
        self.times.reverse()
        return self.times
#########################################################################    
    def getWeekBitMask(self, days):
        sum = 90000000
        for day in days:
            if('Saturday' in day): 
                sum+=1000000
            elif('Sunday' in day):
                sum+=100000
            elif('Monday' in day): 
                sum+=10000
            elif('Tuesday' in day): 
                sum+=1000
            elif('Wednesday' in day): 
                sum+=100
            elif('Thursday' in day): 
                sum+=10
            elif('Friday' in day): 
                sum+=1
        self.weekBitmask=sum
        return self.weekBitmask
#########################################################################
    def getTimeBitMask(self, times):
        sum = 90000
        for time in times:
            if('Breakfast' in time):
                sum+=1000
            elif('Lunch' in time):
                sum+=100
            elif('Snacks' in time):
                sum+=10
            elif('Dinner' in time):
                sum+=1
        self.timeBitmask=sum
        return self.timeBitmask
#########################################################################    
    def setID(self, ID):
        self.ID = ID
#########################################################################
    def isAvailable(self, target):
        for day in self.days:
            if day==target or day=='All':
                return 1
        return 0
#########################################################################
#########################################################################
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
################################################################
def generateDetails(name):
    conn = dbase()
    cursor = conn.getCursor ()
    args = [name,]
    cursor.callproc ("searchFoodWithName", args)
    row = cursor.fetchone()
    newFood = Food(row[1],row[2])
    days = newFood.getWeekdays(row[3])
    times = newFood.getHours(row[4])
    newFood.setID(row[0])
    return newFood
################################################################
def getDetails(request, name):
    newFood=generateDetails(name)    
    return render(request, "food/details.html", context = {'food':newFood, 'message':" "})
###################################################################
def getEditForm(request, name):
    newFood = generateDetails(name)
    return render(request, "food/editForm.html", context = {'food':newFood})
###################################################################
def getEditResponse(request, name):
    if request.method == 'POST':
        newName = request.POST.get('food_name', None)
        price = request.POST.get('food_price', None)
        days=[]
        times=[]
        days=request.POST.getlist('day')
        times=request.POST.getlist('time')
        weekBitmask=Food(newName,price).getWeekBitMask(days)
        timeBitMask=Food(newName,price).getTimeBitMask(times)
        newFood = generateDetails(name)
        conn = dbase()
        cursor=conn.getCursor()
        args=[newFood.ID,newName,price,weekBitmask,timeBitMask,]
        cursor.callproc("updateFood", args)
        conn.commit()
        newFood = generateDetails(newName)
    return render(request, "food/details.html", context = {'food':newFood, 'message':"Updated Successfully"})
##########################################################################
def getWeeklyList(request, day):
    conn = dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select FoodName, FoodPrice, weekBitmask from FoodItem")
    foodList=[]
    weekList={}
    for days in Food.weekDayList:
        weekList[days]=0
    weekList['All']=0
    row = cursor.fetchall()
    for i in row:
        newFood = Food(i[0], i[1])
        dayList = newFood.getWeekdays(i[2])
        weekList['All']+=1
        for days in dayList:
            weekList[days]+=1
        if newFood.isAvailable(day)==1 or day=='All':
            foodList.append(newFood)
        
    return render(request, "food/food.html", context = {'food':foodList, 'week':weekList}) 
#########################################################################






