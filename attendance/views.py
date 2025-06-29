from account.models import Membership, MembershipType, Member
from attendance.models import Attendance
from django.utils.timezone import now
from attendance.models import QRCode
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from attendance.serializers import QRCodeSerializer, AttendanceSerializer
from datetime import date

# Create your views here.

class QRCodeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            qrObject = QRCode.objects.get(member=member)
        except QRCode.DoesNotExist:
            return Response('Account does not have any QR code', status=status.HTTP_404_NOT_FOUND)
        
        if (qrObject.isExpired()):
            qrObject.image.delete()
            qrObject.delete()
            return Response('QR code is expired', status=status.HTTP_410_GONE)
        return Response(QRCodeSerializer(qrObject).data, status=status.HTTP_200_OK)
    
    def post(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            qrObject = QRCode.objects.get(member=member)
            return Response('The account already has a QR Code', status=status.HTTP_409_CONFLICT)
        except:
            qrObject = QRCode(member=Member.objects.get(pk=member))
            qrObject.generate()
            qrObject.setExpirationDate()
            qrObject.save()
            return Response('Success', status=status.HTTP_201_CREATED)


class LoggingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        attendances = Attendance.objects.filter(timeOut=None, date=now())
        ratio = {}
        for attendance in attendances:
            ratio[attendance.member.sex] = ratio.get(attendance.member.sex, 0) + 1
        return Response({'Number' : len(attendances.all()), 'Ratio':ratio}, status=status.HTTP_200_OK)
        
    def post(self, request:Request) -> Response:
        qrCode = request.data.get('qrCode')
        if (not self.request.user.is_superuser):
            return Response('You are not the owner!', status=status.HTTP_403_FORBIDDEN)

        try:
            qrObject = QRCode.objects.get(content=qrCode)
        except QRCode.DoesNotExist:
            return Response('QR code does not exist', status=status.HTTP_404_NOT_FOUND)
        
        if (now().date() > qrObject.expirationDate):
            qrObject.delete()
            return Response('QR code is expired', status=status.HTTP_410_GONE)

        try:
            attendance = Attendance.objects.get(member=qrObject.member, date=now())
            attendance.logOut()
            attendance.save()
            return Response('Successfuly logged out', status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            attendance = Attendance(member=qrObject.member)
            attendance.save()
            data = {}
            data['details'] = 'Successfuly logged in'
            data['name'] = f'{qrObject.member.first_name} {qrObject.member.last_name}'
            membership = Membership.objects.get(member=qrObject.member)
            data['type'] = membership.membershipType.name
            data['price'] = Membership.objects.get(member=qrObject.member).membershipType.price
            if (not membership.membershipType.subscription):
                data['paid'] = False
            else:
                data['expiry'] = membership.expirationDate
                data['paid'] = False if (now().date() > membership.expirationDate) else True
            return Response(data, status=status.HTTP_201_CREATED)
    

class AttendanceView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request:Request, year:int, month:int, day:int) -> Response:
        attendances = Attendance.objects.filter(date=date(year, month, day)).order_by('timeIn')
        data = AttendanceSerializer(attendances, many=True).data
        for attendance in data:
            member = Member.objects.get(pk=attendance['member'])
            attendance['member'] = member.username
        return Response(data, status=status.HTTP_200_OK)
            
