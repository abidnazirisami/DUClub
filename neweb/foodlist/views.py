# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    template = loader.get_template("/home/sami/neweb/foodlist/index.html")
    return HttpResponse(template.render())
    

def showList():
    print "whatcha doin"
