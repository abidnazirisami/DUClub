from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
import MySQLdb
class Food:
    counter=0
    def __init__(self, name, price):
        self.name = name
        self.price = price
        Food.counter += 1

def getPrice(request, name):
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor ()
    cursor.execute ("select FoodPrice from FoodItem where FoodName = '"+name+"'")
    if cursor.rowcount == 0:
        html = "<html><body>%s is not available.</body></html>" % name
    else:
        row = cursor.fetchone()
        html = "<html><body>The Price is %s.</body></html>"% row[0]
    return HttpResponse(html)

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
        html = "<html><body>There is no Food</body></html>" 
    else:
        foodList=[]
        row = cursor.fetchall()
        for i in row:
            if (((i[2]-90000000)/div)>=(1000000/div) and ((i[2]-90000000)/div)%2==1 ) or div==2:
                foodList.append(Food(i[0],i[1]))
                
	return render_to_response("new.html",{'food':foodList}) 

