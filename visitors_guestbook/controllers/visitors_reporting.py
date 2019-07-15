from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ..models import VisitHistory , Visitor

@login_required
def report(request , visitor_id):
    """
    Report a particular visitor
    """
    visitor = Visitor.objects.get(pk=visitor_id)
    visit_history =  visitor.getAllVisitHistory()
    change_details = visitor.getAllVisitorDetailChangeHistory()
    total_visit_for_this_week = visitor.getThisWeekVisitHistory().count()
    total_vist_for_this_month = visitor.getThisMonthVisitHistory().count()
    total_vist = visit_history.count()

    context =  {
        "visitor" : visitor ,
        "visit_history" : visit_history,
        "change_details" : change_details,
        "total_visit_for_this_week" : total_visit_for_this_week,
        "total_vist_for_this_month" : total_vist_for_this_month ,
        "total_vist" : total_vist
    }

    return render(request, 'visitors_guestbook/report_visitor.html', context)

@login_required
def reportAll(request):
    """
    Report all visitors
    """
    vh = VisitHistory()
    visit_history =  vh.getVisitHistories()

    total_visit_today = vh.getTodayVisitorVisit().count()
    total_visit_for_this_week = vh.getThisWeekVisitHistory().count()
    total_vist_for_this_month = vh.getThisMonthVisitHistory().count()
    total_vist = visit_history.count()

    context =  {
        "visit_history" : visit_history,
        "total_visit_today" : total_visit_today,
        "total_visit_for_this_week" : total_visit_for_this_week,
        "total_vist_for_this_month" : total_vist_for_this_month,
        "total_vist" : total_vist
    }
    
    return render(request, 'visitors_guestbook/report.html', context)