from django.contrib import admin
from gym.models import Program, ProgramWorkout, Workout, ProgramWorkoutRecord, TimelineRecord

# Register your models here.


models = [Program, ProgramWorkout, Workout, ProgramWorkoutRecord, TimelineRecord]

for model in models:
    admin.site.register(model)
