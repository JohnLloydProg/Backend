from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.timezone import now
from datetime import timedelta
from account.models import Member
from django.core.files.base import ContentFile
from django.core.files import File
import qrcode

# Create your models here.
def timelineRecordPath(instance, filename):
    return f'user_{str(instance.member.pk)}/qr-code/{filename}'

class QRCode(models.Model):
    """
    Model used to store the QR code for logging purposes.
    """

    content = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    image = models.ImageField(upload_to=timelineRecordPath, null=True, blank=True)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    expirationDate = models.DateField(default=now)

    def generate(self):
        qrImage = qrcode.make(str(self.content))
        qrImage.save('temp-qr.png')
        self.image.save('code.png', File(open('temp-qr.png', 'rb')))

    def setExpirationDate(self):
        self.expirationDate = now().date() + timedelta(days=7)
    
    def isExpired(self):
        return now().date() > self.expirationDate


class Attendance(models.Model):
    """
    Model used to store the date, time-in, and time-out for attendance. It is also the way for tracking the number of members in the gym.
    """

    date = models.DateField(default=now)
    timeIn = models.TimeField(default=now)
    timeOut = models.TimeField(null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def logOut(self):
        self.timeOut = now().time()
    
    def __str__(self):
        return f'{self.member}_{self.date.isoformat()} : {self.timeIn} - {self.timeOut} ({str(self.pk)})'
