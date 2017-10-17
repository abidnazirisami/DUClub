from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from django.template import RequestContext
import MySQLdb
import abc, six
##################################################################################
########################### Singleton Pattern ####################################
##################################################################################
class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
##################################################################################
@six.add_metaclass(abc.ABCMeta)
class dbase():
    conn = MySQLdb.connect (host = "localhost",
                                user = "root",
                                passwd = "ostad21",
                                db = "duclub")
    def getCursor(self):
        cursor = self.conn.cursor()
        return cursor
    def commit(self):
        self.conn.commit()
##################################################################################
##################################################################################
##################################################################################
