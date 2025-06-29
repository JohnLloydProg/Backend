from django.urls import path
from gym import views


urlpatterns = [
    path('programs', views.ProgramsView.as_view(), name='programs'),
    path('program/current', views.CurrentProgramView.as_view(), name='current program'),
    path('program/<int:pk>', views.ProgramView.as_view(), name='program'),
    path('workout/<int:program>', views.ProgramWorkoutCreateView.as_view(), name='workout'),
    path('workout/<int:program>/update/<int:pk>', views.ProgramWorkoutUpdateView.as_view(), name='workout update'),
    path('workout/<int:program>/delete/<int:pk>', views.ProgramWorkoutDeleteView.as_view(), name='workout delete'),
    path('workouts', views.WorkoutsView.as_view(), name='workouts'),
    path('workout-record/<int:programWorkout>', views.ProgramWorkoutRecordsView.as_view(), name='workout records'),
    path('progress', views.TimelineRecordsView.as_view(), name='progress'),
    path('progress/current', views.CurrentTimelineRecordView.as_view(), name='current progresss')

]
