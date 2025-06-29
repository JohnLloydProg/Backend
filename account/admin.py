from django.contrib import admin
from .models import Member, ValidationSession, Membership, MembershipType

# Register your models here.


models = [Member, Membership, MembershipType, ValidationSession]

for model in models:
    admin.site.register(model)
