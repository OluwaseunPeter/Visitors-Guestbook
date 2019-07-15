from django.urls import path

from . import views

app_name = 'visitors_guestbook'
urlpatterns = [
    path('', views.index, name='index'),
    path('visits/', views.reportAll, name='report_all'),
    path('visits/<int:visitor_id>', views.report, name='report_visitor')
]