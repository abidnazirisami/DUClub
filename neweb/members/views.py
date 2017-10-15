# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext

import MySQLdb
import abc, six



###############################################################
################### Strategy Pattern ##########################
###############################################################
###############################################################
class Context:

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self, request, search_id):
        return self._strategy.searchMem(request, search_id)

###############################################################
@six.add_metaclass(abc.ABCMeta)
class SearchClass():


    @abc.abstractmethod
    def searchMem(self, request, search_id):
        pass
###############################################################

class SearchWithName(SearchClass):


    def searchMem(self, request, search_id):
        conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
        cursor = conn.cursor ()
        cursor.execute ("select MemberID, MemberName from Accounts where MemberName like '%%%s%%'" %search_id)
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
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        if search_id[0] <= '9' and search_id[0] >= '0':
            #row = searchWithID(request, search_id)
            context = Context(id_strategy)
        else:
            #row = searchWithName(request, search_id)
            context = Context(name_strategy)
        
        row = context.context_interface(request, search_id)
        for i in row:
            memberList.append(Member(i[0],i[1]))
        return render(request, "searchResults.html",context={'member':memberList}) 
        #return HttpResponse(row)        
################################################################################################        
def searchMember(request):
    return render(request, "search.html")
################################################################
###############################################################
###############################################################
def addMember(request):
    name = request.POST.get('username', None)
    if not name:
        return render(request, "memberForm.html", context={'warning': "Please enter the name of the member"})
    mail = request.POST.get('usermail', None)
    if not mail:
        return render(request, "memberForm.html", context={'warning': "Please enter the E-mail address of the member"})
    cell_no = request.POST.get('contactno', None)
    if not cell_no:
        return render(request, "memberForm.html", context={'warning': "Please enter the Contact No. of the member"})
    present_ad = request.POST.get('userprad', None)
    permanent_ad = request.POST.get('userpmad', None)
    dept = request.POST.get('userdept', None)
    if not dept:
        return render(request, "memberForm.html", context={'warning': "Please enter the name of the Department of the member"})
    designation = request.POST.get('userdesignation', None)
    if not designation:
        return render(request, "memberForm.html", context={'warning': "Please enter the Designation of the member"})
    status = request.POST.get('userstat', None)
    member_type = request.POST.get('usertype', None)
    if not member_type:
        return render(request, "memberForm.html", context={'warning': "Please enter the type of the member"})

    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor()
    args = [name,cell_no,present_ad,permanent_ad,designation,dept,status,mail,member_type,]
    s = cursor.callproc("addMember", args)
    conn.commit()    
    cursor.close()
    conn.close()
    return render(request, "memberSuccess.html", context = {'name': name, 'mail':mail, 'cell_no':cell_no,'present_ad':present_ad,'permanent_ad':permanent_ad,'dept':dept,'designation':designation, 'status': status,'member_type':member_type})
###############################################################
def addMem(request):
    return render(request, "memberForm.html", context={'warning': ""})


