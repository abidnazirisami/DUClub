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

####################################################################
def deleteMemberPage(request):
    return render(request, "deleteMember.html", context={'warning':""})
####################################################################
def updateMemberPage(request):
    return render(request, "updateForm.html", context={'warning':""})
####################################################################
def deleteMember(request):
    memberid = request.POST.get('memberid', None)
    if not memberid:
        return render(request, "deleteMember.html", context={'warning': "Please enter the id of the member"})
 
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor()
    cursor.execute ("select * from Accounts where memberID = "+memberid)
    if cursor.rowcount == 0:
        return render(request, "deleteMember.html", context={'warning': "Please enter a valid ID"})
    else:
        row = cursor.fetchone()
        return render(request, "confirmDelete.html", context = {'name': row[1], 'memberid':row[0],'designation':row[5],'dept':row[6]})
##########################################################
def deleteMem(request):
    memberid = request.POST.get('memberid', None)
    if not memberid:
        return render(request, "deleteMember.html", context={'warning': "Please enter the id of the member"})
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor()
    args = [memberid,]
    s = cursor.callproc("deleteMember", args)
    conn.commit()    
    cursor.close()
    conn.close()
    return render(request, "deleteSuccess.html")
###################################################################
def updateMember(request):
    memberid = request.POST.get('memberid', None)
    if not memberid:
        return render(request, "updateForm.html", context={'warning': "Please enter the id of the member"})
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "ostad21",
                            db = "duclub")
    cursor = conn.cursor()
    cursor.execute ("select * from Accounts where memberID = "+memberid)
    if cursor.rowcount == 0:
        return render(request, "updateMember.html", context={'warning': "Please enter a valid ID"})
    row = cursor.fetchone()
    name = request.POST.get('username', None)
    if not name:
        name = row[1]
    mail = request.POST.get('usermail', None)
    if not mail:
        mail = row[8]
    cell_no = request.POST.get('contactno', None)
    if not cell_no:
        cell_no = row[2]
    present_ad = request.POST.get('userprad', None)
    if not present_ad:
	present_ad = row[3]
    permanent_ad = request.POST.get('userpmad', None)
    if not permanent_ad:
	permanent_ad = row[4]
    dept = request.POST.get('userdept', None)
    if not dept:
        return render(request, "upadteForm.html", context={'warning': "Please enter the name of the Department of the member"})
    designation = request.POST.get('userdesignation', None)
    if not designation:
        return render(request, "updateForm.html", context={'warning': "Please enter the Designation of the member"})
    status = request.POST.get('userstat', None)
    if not status:
        return render(request, "updateForm.html", context={'warning': "Please enter the Status of the member"})
    member_type = request.POST.get('usertype', None)
    if not member_type:
        return render(request, "updateForm.html", context={'warning': "Please enter the type of the member"})

    args = [memberid,name,cell_no,present_ad,permanent_ad,designation,dept,status,mail,member_type,]
    s = cursor.callproc("updateMember", args)
    conn.commit()    
    cursor.close()
    conn.close()
    return render(request, "updateSuccess.html", context = {'name': name, 'mail':mail, 'cell_no':cell_no,'present_ad':present_ad,'permanent_ad':permanent_ad,'dept':dept,'designation':designation, 'status': status,'member_type':member_type})
