from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from attendance.models import Attendance
from account.models import Member, Membership, MembershipType, MemberCheckout
from sales.models import Sale
from sales.serializers import SaleSerializer
from gym.models import ProgramWorkout
from django.utils.timezone import now

def objectsThisMonth(_object, month, **kwargs):
    objects = []
    for obj in _object.objects.filter(**kwargs):
        if (obj.date.month == month):
            objects.append(obj)
    return objects

class PeakActivityView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request:Request, month:int) -> Response:
        hourRecords = {hour:0 for hour in range(0, 24)}
        hours = []
        for attendance in objectsThisMonth(Attendance, month):
            if (attendance.timeOut):
                hours.append((attendance.timeIn.hour, attendance.timeOut.hour))
        for inOut in hours:
            for inHour in range(inOut[0], inOut[1]+1):
                hourRecords[inHour] += 1
        
        dayRecords = {day:0 for day in range(7)}
        days = [attendance.date.weekday() for attendance in objectsThisMonth(Attendance, month)]
        for day in days:
            dayRecords[day] += 1
        return Response({'hours': hourRecords, 'days': dayRecords}, status=status.HTTP_200_OK)


class MembersReportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request:Request) -> Response:
        response = {}
        response['number'] = len(Member.objects.all())
        response['demographics'] = {}
        response['demographics']['M'] = len(Member.objects.filter(sex='Male'))
        response['demographics']['F'] = len(Member.objects.filter(sex='Female'))
        response['memberships'] = {}
        for membership in Membership.objects.all():
            response['memberships'][membership.membershipType.name] = response['memberships'].get(membership.membershipType.name, 1) + 1
        response['workouts'] = {pType:0 for pType in ['L', 'C', 'U', 'PS', 'PL']}
        for programWorkout in ProgramWorkout.objects.all():
            response['workouts'][programWorkout.workout.type] += 1
        return Response(response, status=status.HTTP_200_OK)


class SalesReportView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request:Request, month:int) -> Response:
        sales = []
        for sale in Sale.objects.all():
            if sale.date.month == month:
                sales.append(sale)
        return Response(SaleSerializer(sales, many=True).data, status=status.HTTP_200_OK)

