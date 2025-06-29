from django.urls import path
from scheduling import views


urlpatterns = [
    path('schedules', views.SchedulesView.as_view(), name='schedule'),
    path('schedule/next', views.NextScheduleView.as_view(), name='next schedule'),
    path('schedule/create', views.ScheduleCreateView.as_view(), name='schedule create'),
    path('schedule/update/<int:pk>', views.ScheduleUpdateDestroyView.as_view(), name='schedule update'),

]
