# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext

import MySQLdb
import abc, six

###############################################################################################

def billForm(request):
    return render(request, "billForm.html", context ={'warning':""})

###############################################################################################

def submitBill(request):
    name = request.POST.get('itemname',None)
    if not name:
        return render(request, "billForm.html", context={'warning':"Please insert an item name"})
    return render(request, "billCreated.html", context = {'name': name})

###############################################################################################
