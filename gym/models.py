from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from datetime import timedelta
from account.models import Member

# Create your models here.
weekdays = {
            0 : "Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 
            4:"Friday", 5:'Saturday', 6:'Sunday'
            }

def timelineRecordPath(instance, filename):
    return f'user_{str(instance.member.pk)}/timeline/{now().isoformat()}-{filename}'


class Program(models.Model):
    day = models.IntegerField(
        choices=weekdays,
        null=True
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f'{weekdays[self.day]} ({str(self.pk)})' if (self.day) else f'No Day ({str(self.pk)})'


class Workout(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=5, choices={
        "L":"Lower",
        "U":"Upper",
        "C":"Core",
        "PS":"Push",
        "PL":"Pull"
        }
    )
    time = models.BooleanField()
    sets = models.BooleanField()
    reps = models.BooleanField()
    weight = models.BooleanField()
    distance = models.BooleanField()

    def __str__(self):
        return f'{self.name} ({str(self.pk)})'


class ProgramWorkout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    details = models.JSONField()


class ProgramWorkoutRecord(models.Model):
    date = models.DateField(default=now)
    programWorkout = models.ForeignKey(ProgramWorkout, on_delete=models.CASCADE)
    details = models.JSONField()


class TimelineRecord(models.Model):
    date = models.DateField(default=now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to=timelineRecordPath, null=True, blank=True)