from django.urls import path
from analytics import views

urlpatterns = [
    path('peak/<int:year>/<int:month>', views.PeakActivityView.as_view(), name='peak activity'),
    path('members/report', views.MembersReportView.as_view(), name='members report'),
    path('sales/<int:year>/<int:month>', views.SalesReportView.as_view(), name='sales report'),
    path('report/<int:year>/<int:month>', views.PrintReportView.as_view(), name='print report')
]
