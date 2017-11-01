# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.core.mail import EmailMessage
import MySQLdb
import abc, six
from django.shortcuts import render
from members.views import *
import threading
import time
from smtplib import SMTPException
exitFlag = 0
# Create your views here.

def mailHome(request):
    memberList=getMembers('')
    membersJSON = {}
    for member in memberList:
        membersJSON[member.name]=0
    return render(request, "mail/mailHome.html",context= {'members':membersJSON})
###################################################################
def sendMail(request):
   subject = request.POST.get('subject', None)
   body = request.POST.get('message', None)
   exitFlag = 0
   mailingThread = MailingThread(1, "mailSender",30,subject,body,request)
   mailingThread.start()
   return render(request, "mail/sent.html")

######################################################################
class MailingThread (threading.Thread):
   def __init__(self, threadID, name, counter,subject,body,request):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.subject = subject
      self.body = body
      self.request = request
   def run(self):
      mailSender(self, self.name, self.counter, 10,self.subject,self.body,self.request)
#############################################################################      
def mailSender(mailingThread, threadName, counter, delay,subject,body,request):
    flag = 0   
    while counter > 0: 
        if sendMail2(subject,body,request) == 1 :
            counter = 0
            flag = 1	  
        time.sleep(delay)    
        counter += 1
###########################################################################
def sendMail2(subject,body,request):    
   
   try:
       email = EmailMessage(subject, body, to=["raidanahian@gmail.com","abidnazirisami@gmail.com","sdp02342017@gmail.com"])
       email.send()
       return 1
   except:
       print('There was an error sending an email: ')
   return 0
   
