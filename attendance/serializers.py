from rest_framework import serializers
from attendance.models import Attendance, QRCode


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['content', 'member', 'expirationDate', 'image']
        extra_kwargs = {
            'content':{'read_only':True},
            'member':{'read_only':True},
            'expirationDate':{'read_only':True}
            }


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'timeIn', 'timeOut', 'member']
        extra_kwargs = {
            'member':{'read_only':True},
            'date':{'read_only':True},
            'timeIn':{'read_only':True},
            'timeOut':{'read_only':True}
            }
