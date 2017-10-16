# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext

import MySQLdb
import abc, six


# Create your views here.
###############################################################################
def loungeHome(request):
    return render(request, "loungeHome.html")
################################################################################

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
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeName like '%%%s%%'" %search_id)
        return cursor.fetchall() 

###############################################################
class SearchWithID(SearchClass):

     def searchLng(self, request, search_id):
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge where LoungeID = '%s'" %search_id)
        return cursor.fetchall()

###############################################################
class SearchAll(SearchClass):

     def searchLng(self, request, search_id):
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select LoungeID, LoungeName from Lounge")
        return cursor.fetchall()



################################################################
class Lounge:
    counter=0
    def __init__(self, id, name):
        self.name = name
        self.id = id
        Lounge.counter += 1
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
        return render(request, "LoungeResult.html",context={'lounge':loungeList})    
##################################################################################################################
################################################################
###############################################################
###############################################################
def addLounge(request):
    name = request.POST.get('username', None)
    if not name:
        return render(request, "loungeForm.html", context={'warning': "Please enter the name of the lounge"})
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor()
    args = [name,]
    s = cursor.callproc("addLounge", args)
    conn.commit()    
    cursor.close()
    conn.close()
    return render(request, "loungeSuccess.html", context = {'name': name})
###############################################################
def addLng(request):
    return render(request, "loungeForm.html", context={'warning': ""})

####################################################################
###############################################################
