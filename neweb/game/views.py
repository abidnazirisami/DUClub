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

define gameHome:
    return render(request, "game/game.html");


###############################################################
################### Strategy Pattern ##########################
###############################################################
###############################################################
class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self, request, search_id):
        return self._strategy.searchGame(request, search_id)

###############################################################
@six.add_metaclass(abc.ABCMeta)
class SearchClass():


    @abc.abstractmethod
    def searchGame(self, request, search_id):
        pass
###############################################################

class SearchWithName(SearchClass):


    def searchGame(self, request, search_id):
        conn = Singleton.dbase()
        cursor = conn.getCursor()
        cursor.execute ("select GameID, GameName from GameTable where GameName like '%%%s%%'" %search_id)
        return cursor.fetchall() 

###############################################################
class SearchWithID(SearchClass):

     def searchMem(self, request, search_id):
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select MemberID, MemberName from Accounts where MemberID = '%s'" %search_id)
        return cursor.fetchall()

###############################################################
class SearchAll(SearchClass):

     def searchMem(self, request, search_id):
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select MemberID, MemberName from Accounts")
        return cursor.fetchall()



################################################################
class Member:
    counter=0
    def __init__(self, id, name):
        self.name = name
        self.id = id
        Member.counter += 1
########################################################################################################
def search(request):
    memberList = []

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
            memberList.append(Member(i[0],i[1]))
        return render(request, "searchResults.html",context={'member':memberList})    
################################################################################################        
def memberHome(request):
    return render(request, "members.html")
################################################################
###############################################################
###############################################################

