from django.core.management.base import BaseCommand
from account.models import MembershipType, Membership
from attendance.models import Attendance
from sales.models import Sale
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Tallies the non-subscription attendance of all members into a sales record'

    def handle(self, *args, **options):
        right_now = now()
        sales:dict[str, Sale] = {}
        for attendance in Attendance.objects.filter(date=right_now.date()):
            membership = Membership.objects.get(member=attendance.member)
            if (not membership.membershipType.subscription):
                sales[membership.membershipType.name] = sales.get(membership.membershipType.name, Sale(amount=0, description=f"Membership {membership.membershipType.name}"))
                sales[membership.membershipType.name].amount += membership.membershipType.price
        for sale in sales.values():
            sale.save()
        self.stdout.write('Done tallying attendances')
