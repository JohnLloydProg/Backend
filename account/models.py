from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.

def userProfilePath(instance, filename:str) -> str:
    return f'user_{str(instance.user.id)}/{filename}'


class ValidationSession(models.Model):
    """
    Model responsible for the validating the user email and linking it to the registration page
    """

    validationCode = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(max_length=255, verbose_name="Email")
    expirationDate = models.DateField(null=True, verbose_name='Expiration Date')

    def setExpirationDate(self) -> None:
        self.expirationDate = now().date() + timedelta(days=1)


class Member(User):
    """
    Model used for member accounts. Also used for authentication. Inherits from the User class from django.
    """
    class Meta:
        verbose_name = 'Member'

    birthDate = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    mobileNumber = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gymTrainer = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True)
    sex = models.CharField(max_length=30, default='NA')
    is_trainer = models.BooleanField(default=False)
    facebookAccount = models.URLField(null=True, blank=True)
    profilePic = models.ImageField(upload_to=userProfilePath, null=True, blank=True)

    def __str__(self):
        return f'{self.username} ({str(self.pk)})'


class MembershipType(models.Model):
    name = models.CharField(max_length=50)
    subscription = models.BooleanField()
    price = models.FloatField()


class Membership(models.Model):
    """
    Model for the membership details. Also the parent model for daily and monthly memberships
    """

    startDate = models.DateField(auto_now_add=True, editable=False)
    member = models.OneToOneField(Member, on_delete=models.CASCADE, editable=False)
    membershipType = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    expirationDate = models.DateField(default=now)

    class Meta:
        ordering = ['startDate']
    
    def extendExpirationDate(self) -> None:
        self.expirationDate += timedelta(days=30)


class MemberCheckout(models.Model):
    checkoutId = models.CharField(max_length=200, primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
