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
    dayTimeList = ['Breakfast','Lunch','Snacks','Dinner']
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.days=[]
        self.times=[]
        self.available="Not Available"
#########################################################################      
    
    def getWeekdays(self, bitMask):
        bitMask -= 90000000
        weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] # This is for the datetime.datetime.today.weekday[] function
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
        mask = 90000000
        for day in days:
            counter = 0
            for weekDay in self.weekDayList:
                if weekDay in day:
                    mask+=(10**(6-counter))
                counter+=1
        self.weekBitmask=mask
        return self.weekBitmask
#########################################################################
    def getTimeBitMask(self, times):
        mask = 90000
        for time in times:
            counter = 0
            for dayTime in self.dayTimeList:
                if dayTime in time:
                    mask+=(10**(3-counter))
                counter+=1
        self.timeBitmask=mask
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
        
    return render(request, "food/food.html", context = {'food':foodList, 'week':weekList, 'currentDay':day}) 
#########################################################################

def getAddForm(request):
    newFood = Food("","")
    return render(request, "food/addForm.html", context = {'food':newFood})
###################################################################
def getAddResponse(request):
    newFood = Food("","")
    if request.method == 'POST':
        newName = request.POST.get('food_name', None)
	if newName == "":
            return render(request, "food/addForm.html", context = {'food':newFood,'warning':"Please give a name"})
        price = request.POST.get('food_price', None)
        if price == "":
            return render(request, "food/addForm.html", context = {'food':newFood,'warning':"Place add a price"})
        days=[]
        times=[]
        days=request.POST.getlist('day')
        times=request.POST.getlist('time')
        weekBitmask=Food(newName,price).getWeekBitMask(days)
        timeBitMask=Food(newName,price).getTimeBitMask(times)
        conn = dbase()
        cursor=conn.getCursor()
        args=[newName,price,weekBitmask,timeBitMask,]
        cursor.callproc("addFoodItem", args)
        conn.commit()
        newFood = generateDetails(newName)
    return render(request, "food/details.html", context = {'food':newFood, 'message':"Added Successfully"})
###################################################################
def deletePrompt(request, name):
    newFood = generateDetails(name)
    return render(request, "food/confirmDelete.html", context = {'food': newFood})
###################################################################
def deleteFood(request):
    foodName = request.POST.get('foodname', None)
    conn = dbase()
    cursor = conn.getCursor()
    args = [foodName,]
    s = cursor.callproc("deleteFood", args)
    conn.commit()    
    cursor.close()
    return render(request, "food/deleteSuccess.html")




