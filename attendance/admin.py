from django.contrib import admin
from .models import Attendance, QRCode

# Register your models here.


models = [Attendance, QRCode]

for model in models:
    admin.site.register(model)
