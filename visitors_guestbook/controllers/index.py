from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import logout
from datetime import datetime

import base64

from ..forms.vistors_form import VisitorsForm
from ..forms.visitors_history_form import VisitHistoryForm
from ..models import Visitor , VisitHistory , VisitorDetailChangeHistory , VISITORS_ADDRESS , VISITORS_NAME



def index(request):

    #if there is an autheticated session , we log the user out 
    #because we dont want the visitor to have access to the report pages
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        visitor_form  =  VisitorsForm(request.POST)
        history_form =  VisitHistoryForm(request.POST)
        if visitor_form.is_valid() and history_form.is_valid():
            
            #lets check if we have a visitor with same email
            #and update their details if available
            email = str.strip(visitor_form.cleaned_data["email"])
            email = str.lower(email)
            visitor =  Visitor().getVisitorWithEmail(email)

            info = None

            if visitor is None:
                visitor =  visitor_form.instance
                visitor.email = email
                visitor.save()
                
                visit_history =  history_form.instance
                visit_history.visitor = visitor
                visit_history.save()

            else:
                
                #lets check if this visitor has vist today
                visit_history =  VisitHistory().getTodayVisitorVisit(visitor=visitor)
                if visit_history.count() >= 1:
                    visit_history = visit_history[0]
                    info =  "You have previously been checked in"
                else:
                    visit_history =  history_form.instance
                    visit_history.visitor = visitor
                    visit_history.save()

                #lets compare if the visitor address and 
                #name has change from the last time visit
                visitor_need_update =  False
                last_address = visitor.address
                address = str.strip(visitor_form.cleaned_data["address"])

                if last_address != address:
                    #lets create an entry for this change
                    changeHistory =  VisitorDetailChangeHistory()
                    changeHistory.field =  VISITORS_ADDRESS
                    changeHistory.from_value = visitor.address
                    changeHistory.to_value = address
                    changeHistory.visitor = visitor
                    changeHistory.history = visit_history
                    changeHistory.save()

                    #update vistor record
                    visitor.address = address
                    visitor_need_update =  True

                last_name = visitor.name
                name = str.strip(visitor_form.cleaned_data["name"])

                if last_name != name:
                    #lets create an entry for this change
                    changeHistory =  VisitorDetailChangeHistory()
                    changeHistory.field =  VISITORS_NAME
                    changeHistory.from_value = visitor.name
                    changeHistory.to_value = name
                    changeHistory.visitor = visitor
                    changeHistory.history = visit_history
                    changeHistory.save()
                    
                    #update vistor record
                    visitor.name = name
                    visitor_need_update =  True

                if visitor_need_update:
                    visitor.save()
            
            context = {
                    "visitor_form" : VisitorsForm(),
                    "history_form": VisitHistoryForm(),
                    "success" : f"You are welcome {visitor.name}",
                    "info" : info
            }

            return render(request, 'visitors_guestbook/index.html', context)

    else:
        visitor_form =  VisitorsForm()
        history_form = VisitHistoryForm()

    context = {
        "visitor_form" : visitor_form,
        "history_form": history_form
    }
    return render(request, 'visitors_guestbook/index.html', context)