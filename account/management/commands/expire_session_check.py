from django.core.management.base import BaseCommand
from account.models import ValidationSession
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Removes expired Validation Sessions in the database'

    def handle(self, *args, **options):
        right_now = now()
        for session in ValidationSession.objects.all():
            if (right_now.date() > session.expirationDate):
                session.delete()
        self.stdout.write('Done removing expired validation sessions.')
