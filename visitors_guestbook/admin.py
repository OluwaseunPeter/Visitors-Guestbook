from django.contrib import admin

# Register your models here.
from .models import VisitHistory , Visitor , VisitorDetailChangeHistory

class VisitorAdmin(admin.ModelAdmin): 
    list_display = ['name', 'email' , "address" , "date_created"]

class VisitHistoryAdmin(admin.ModelAdmin): 
    list_display = ["visitor_name" , "visitor_email" ,  "to_see" , "visit_purpose" , "check_in_date"]
    
    def visitor_name(self, obj): 
        return obj.visitor.name
    
    def visitor_email(self, obj): 
        return obj.visitor.email

class VisitorDetailChangeHistoryAdmin(admin.ModelAdmin): 
    list_display = ["visitor_name" , "visitor_email" , "field" , "change_from" , "change_to" , "date_created"]

    def visitor_name(self, obj): 
        return obj.visitor.name
    
    def visitor_email(self, obj): 
        return obj.visitor.email

    def change_from(self, obj): 
        return obj.from_value
    
    def change_to(self, obj): 
        return obj.to_value

admin.site.register(Visitor , VisitorAdmin )
admin.site.register(VisitHistory , VisitHistoryAdmin)
admin.site.register(VisitorDetailChangeHistory, VisitorDetailChangeHistoryAdmin )
