from django.db import models
from account.models import Member

# Create your models here.


class Schedule(models.Model):
    trainee = models.ForeignKey(Member, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

