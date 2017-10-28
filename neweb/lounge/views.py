# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from neweb.views import *
import MySQLdb
import abc, six

###############################################################################
class Lounge:
    def __init__(self, id, name):
        self.name = name
        self.id = id
###############################################################################
def loungeHome(request):
    conn = dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select LoungeID, LoungeName from Lounge")
    loungeList=[]
    row = cursor.fetchall()
    for i in row:
        newLounge = Lounge(i[0], i[1])
        loungeList.append(newLounge)
    return render(request, "lounge/loungeHome.html" ,  context={'lounge': loungeList})
################################################################################
def addLoungePage(request):
    return render(request, "lounge/loungeForm.html", context={'warning':""})
################################################################################
def deleteLoungePage(request,name):
    return render(request, "lounge/deleteLounge.html", context={'warning':"",'id': name})
################################################################################
def updateLoungePage(request,name):
    return render(request, "lounge/updatelounge.html", context={'warning':"", 'id' : name})
###############################################################
################### Strategy Pattern ##########################
###############################################################
###############################################################
class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self, request, search_id):
        return self._strategy.searchLng(request, search_id)

###############################################################
@six.add_metaclass(abc.ABCMeta)
class SearchClass():


    @abc.abstractmethod
    def searchLng(self, request, search_id):
        pass
###############################################################

class SearchWithName(SearchClass):


    def searchLng(self, request, search_id):
        conn = dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeName like '%%%s%%'" %search_id)
        return cursor.fetchall() 

###############################################################
class SearchWithID(SearchClass):

     def searchLng(self, request, search_id):
        conn = dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeID = '%s'" %search_id)
        return cursor.fetchall()

###############################################################
class SearchAll(SearchClass):

     def searchLng(self, request, search_id):
        conn = dbase()
        cursor = conn.getCursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge")
        return cursor.fetchall()
########################################################################################################
def search(request):
    loungeList = []

    name_strategy = SearchWithName()
    id_strategy = SearchWithID()
    all_strategy = SearchAll()
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        if not search_id:
            context = Context(all_strategy)
        elif search_id[0] <= '9' and search_id[0] >= '0':
            context = Context(id_strategy)
        else:
            context = Context(name_strategy)
        
        row = context.context_interface(request, search_id)
        for i in row:
            loungeList.append(Lounge(i[0],i[1]))
        return render(request, "lounge/LoungeResult.html",context={'lounge':loungeList})    
##################################################################################################################
################################################################
###############################################################
###############################################################
def addLounge(request):
    name = request.POST.get('username', None)
    if not name:
        return render(request, "lounge/loungeForm.html", context={'warning': "Please enter the name of the lounge"})
    conn = dbase()
    cursor = conn.getCursor()
    args = [name,]
    s = cursor.callproc("addLounge", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "lounge/loungeSuccess.html", context = {'name': name})
###############################################################
def addLng(request):
    return render(request, "lounge/loungeForm.html", context={'warning': ""})

####################################################################
###############################################################

def deleteLounge(request):
    loungeid = request.POST.get('loungeid', None)
    if not Loungeid:
        return render(request, "lounge/deleteLounge.html", context={'warning': "Please enter the id of the Lounge"})
 
    conn = dbase()
    cursor = conn.getCursor()
    cursor.execute ("select * from Lounge where LoungeID = "+Loungeid)
    if cursor.rowcount == 0:
        return render(request, "lounge/deleteLounge.html", context={'warning': "Please enter a valid ID"})
    else:
        row = cursor.fetchone()
        return render(request, "lounge/confirmLounge.html", context = {'name': row[1], 'loungeid':row[0]})
##########################################################
def deleteLng(request,loungeid):

    conn = dbase()
    cursor = conn.getCursor()
    args = [loungeid,]
    s = cursor.callproc("deletelounge", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "lounge/deleteSuccess.html")
#################################################################
def updateLounge(request):
    loungeid = request.POST.get('loungeid', None)
    if not loungeid:
        return render(request, "lounge/updatelounge.html", context={'warning': "Please enter the id of the lounge"})
    conn = dbase()
    cursor = conn.getCursor()
    cursor.execute ("select * from Lounge where loungeID = "+loungeid)
    if cursor.rowcount == 0:
        return render(request, "lounge/updatelounge.html", context={'warning': "Please enter a valid ID"})
    row = cursor.fetchone()
    name = request.POST.get('name', None)
    if not name:
        name = row[1]
    args = [loungeid,name]
    s = cursor.callproc("updateLounge", args)
    conn.commit()    
    cursor.close()
    
    return render(request, "lounge/LoungeSuccess.html", context = {'name': name})
######################################################################
def generateDetails(loungeid):
    conn = dbase()
    cursor = conn.getCursor ()
    cursor.execute ("select * from Lounge where loungeID = "+loungeid)
    row = cursor.fetchone()
    newLounge = Lounge(row[0],row[1])
    return newLounge
################################################################
def getDetails(request, name):
    newLounge=generateDetails(name)    
    return render(request, "lounge/details.html", context = {'lounge':newLounge, 'message':" "})
