from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsTrainer
from scheduling.serializers import ScheduleSerializer
from scheduling.models import Schedule
from account.models import Member
from rest_framework import status
from django.utils.timezone import now

# Create your views here.


class SchedulesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    
    def get(self, request:Request) -> Response:
        schedules = []
        try:
            trainer = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Trainer does not exist', status=status.HTTP_404_NOT_FOUND)
        
        for schedule in Schedule.objects.all().order_by('datetime'):
            if (schedule.trainee.gymTrainer == trainer and now() <= schedule.datetime):
                schedules.append(ScheduleSerializer(schedule).data)
        return Response(schedules, status=status.HTTP_200_OK)


class NextScheduleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        scheduleObjects = Schedule.objects.filter(trainee=member).order_by('datetime')
        if not scheduleObjects:
            return Response('No schedules found for this member', status=status.HTTP_404_NOT_FOUND)
        schedules = []
        for schedule in scheduleObjects:
            if now() <= schedule.datetime:
                schedules.append(schedule)
        return Response(ScheduleSerializer(schedules[0]).data, status=status.HTTP_200_OK)


class ScheduleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsTrainer]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class ScheduleUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

