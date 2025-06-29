from django.core.management.base import BaseCommand
from attendance.models import QRCode
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Removes expired QR codes entries in the database'

    def handle(self, *args, **options):
        right_now = now()
        for qrCode in QRCode.objects.all():
            if (right_now.date() > qrCode.expirationDate):
                qrCode.image.delete()
                qrCode.delete()
        self.stdout.write('Done removing expired QR codes')

