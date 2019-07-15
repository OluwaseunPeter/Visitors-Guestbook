from django.db import models
from django.utils import timezone
from datetime import date, timedelta

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True , null = False , blank= False)
    address = models.CharField(max_length=200)
    
    date_created = models.DateTimeField( default =  timezone.now , editable=False)
    
    deleted =  models.BooleanField(default=False , editable=False)
    deleted_date = models.DateTimeField(null =  True , editable=False)

    def __str__(self):
        return f' {self.name} -  {self.email}'

    def getVisitorWithEmail(self, email):
        lower_case  =  str.lower(email)
        visitors = Visitor.objects.filter(
            email = lower_case 
        )
        if(len(visitors) >= 1):
            return visitors[0]
        return None

    def getAllVisitHistory(self):
        return self.visithistory_set.filter(
            deleted = False ,
        ).order_by('-check_in_date')

    def getThisWeekVisitHistory(self):
        today =  date.today()
        _, _, day_of_week = today.isocalendar()
        this_week = today - timedelta(days= day_of_week - 1)
        return self.visithistory_set.filter(
            deleted = False ,
            check_in_date__gt = this_week
        ).order_by('-check_in_date')
    
    def getThisMonthVisitHistory(self):
        today =  date.today()
        return self.visithistory_set.filter(
            deleted = False ,
            check_in_date__gte = date(today.year, today.month, 1)
        ).order_by('-check_in_date')

    def getAllVisitorDetailChangeHistory(self):
        return self.visitordetailchangehistory_set.filter(
            deleted = False ,
        ).order_by('-date_created')