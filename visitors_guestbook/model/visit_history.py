from django.db import models
from django.utils import timezone
from datetime import date, timedelta

from ..models import Visitor


class VisitHistory(models.Model):
    visitor =  models.ForeignKey(Visitor , on_delete = models.CASCADE)
    to_see =  models.CharField(max_length=100)
    visit_purpose = models.CharField(max_length=100)
    comment = models.TextField(max_length=200 , null=True , blank=True)

    date_created = models.DateTimeField(default =  timezone.now , editable=False)

    check_in_date = models.DateTimeField(default =  timezone.now , editable=False)
    check_out_date = models.DateTimeField(null = True , editable=False)

    deleted =  models.BooleanField(default=False , editable=False)
    deleted_date = models.DateTimeField(null =  True , editable=False)

    def getVisitHistories(self):
        visit_history =  VisitHistory.objects.filter(
            deleted = False ,
            visitor__deleted = False 
        ).order_by('-check_in_date')
        return visit_history
    
    def getThisWeekVisitHistory(self):
        today =  date.today()
        _, _, day_of_week = today.isocalendar()
        this_week = today - timedelta(days= day_of_week - 1)
        return VisitHistory.objects.filter(
            deleted = False ,
            check_in_date__gt = this_week
        ).order_by('-check_in_date')
    
    def getThisMonthVisitHistory(self):
        today =  date.today()
        return VisitHistory.objects.filter(
            deleted = False ,
            check_in_date__gte = date(today.year, today.month, 1)
        ).order_by('-check_in_date')
    
    def getTodayVisitorVisit(self , visitor = None):
        if visitor is not None :
            return VisitHistory.objects.filter(
                deleted = False ,
                visitor = visitor , 
                check_in_date__gte = date.today()
            )
        else:
            return VisitHistory.objects.filter(
                deleted = False ,
                check_in_date__gte = date.today()
            )
    
    def __str__(self):
        return f"{self.visitor.name} - To see: {self.to_see}, Visit Purpose: {self.visit_purpose}"