from account.models import Member
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from gym.serializers import ProgramSerializer, ProgramWorkoutSerializer, WorkoutSerializer, ProgramWorkoutRecordSerializer, TimelineRecordSerializer
from django.utils.timezone import now
from gym.models import Program, ProgramWorkout, Workout, ProgramWorkoutRecord, TimelineRecord
from django.core.files.base import ContentFile
import base64

# Create your views here.


class ProgramsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        id = self.request.user
        member_id = request.query_params.get('user', -1)
        if (member_id != -1):
            try:
                user = Member.objects.get(pk=self.request.user)
            except Member.DoesNotExist:
                return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
            if (user.is_trainer):
                id = int(member_id)
            else:
                return Response('You are not authorized to view this member\'s programs', status=status.HTTP_403_FORBIDDEN)

        try:
            member = Member.objects.get(pk=id)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        programs = Program.objects.filter(member=member)
        data = []
        for program in programs:
            programData = ProgramSerializer(program).data
            programWorkouts = ProgramWorkout.objects.filter(program=program)
            programData['workouts'] = [{'name':programWorkout.workout.name, 'type':programWorkout.workout.type} for programWorkout in programWorkouts]
            data.append(programData)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request:Request) -> Response:
        id = self.request.user
        member_id = request.query_params.get('user', -1)
        if (member_id != -1):
            try:
                user = Member.objects.get(pk=self.request.user)
            except Member.DoesNotExist:
                return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
            if (user.is_trainer):
                id = int(member_id)
            else:
                return Response('You are not authorized to create a program on this member\'s account', status=status.HTTP_403_FORBIDDEN)

        try:
            member = Member.objects.get(pk=id)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)

        program = Program(member=member)
        program.save()
        return Response('Successfully Created', status=status.HTTP_201_CREATED)


class CurrentProgramView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            program = Program.objects.get(member=member, day=now().weekday())            
        except Program.DoesNotExist:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        programWorkouts = ProgramWorkout.objects.filter(program=program)
        data = {'day':program.day, 'workouts':[]}
        for programWorkout in programWorkouts:
            data['workouts'].append({programWorkout.workout.name:programWorkout.details, 'type':programWorkout.workout.type})
        return Response(data, status=status.HTTP_200_OK)


class ProgramView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request:Request, pk:int) -> Response:
        id = self.request.user
        member_id = request.query_params.get('user', -1)
        if (member_id != -1):
            try:
                user = Member.objects.get(pk=self.request.user)
            except Member.DoesNotExist:
                return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
            if (user.is_trainer):
                id = int(member_id)
            else:
                return Response('You are not authorized to create a program on this member\'s account', status=status.HTTP_403_FORBIDDEN)

        try:
            member = Member.objects.get(pk=id)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            program = Program.objects.get(member=member, pk=pk)
        except Program.DoesNotExist:
            return Response("Program does not exist or Program is not the member's", status=status.HTTP_404_NOT_FOUND)
        
        day = request.data.get('day', -1)
        if (day < 0):
            return Response("Please provide the day to update", status=status.HTTP_400_BAD_REQUEST)
        
        program.day = day
        program.save()
        return Response(ProgramSerializer(program).data, status=status.HTTP_200_OK)
    
    def delete(self, request:Request, pk:int) -> Response:
        id = self.request.user
        member_id = request.query_params.get('user', -1)
        if (member_id != -1):
            try:
                user = Member.objects.get(pk=self.request.user)
            except Member.DoesNotExist:
                return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
            if (user.is_trainer):
                id = int(member_id)
            else:
                return Response('You are not authorized to create a program on this member\'s account', status=status.HTTP_403_FORBIDDEN)

        try:
            member = Member.objects.get(pk=id)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            program = Program.objects.get(member=member, pk=pk)
        except Program.DoesNotExist:
            return Response("Program does not exist or Program is not the member's", status=status.HTTP_404_NOT_FOUND)
        
        program.delete()
        return Response('Successfully Deleted', status=status.HTTP_204_NO_CONTENT)


class ProgramWorkoutCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgramWorkoutSerializer
    
    def get(self, request:Request, program:int) -> Response:
        programWorkouts = ProgramWorkoutSerializer(ProgramWorkout.objects.filter(program=program), many=True).data
        for programWorkout in programWorkouts:
            programWorkout['workout'] = WorkoutSerializer(Workout.objects.get(pk=programWorkout['workout'])).data
        return Response(programWorkouts, status=status.HTTP_200_OK)

    def post(self, request:Request, program:int) -> Response:
        try:
            program = Program.objects.get(pk=program)
        except Program.DoesNotExist:
            return Response('Program does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            workout = Workout.objects.get(pk=request.data.get('workout'))
        except Workout.DoesNotExist:
            return Response('Workout does not exist', status=status.HTTP_404_NOT_FOUND)

        programWorkout = ProgramWorkout(workout=workout, program=program, details=request.data.get('details'))
        programWorkout.save()
        return Response(ProgramWorkoutSerializer(programWorkout).data, status=status.HTTP_201_CREATED)


class ProgramWorkoutUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request:Request, program:int, pk:int) -> Response:
        try:
            programObject = Program.objects.get(pk=program)
        except Program.DoesNotExist:
            return Response('Program does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            programWorkout = ProgramWorkout.objects.get(program=programObject, pk=pk)
        except ProgramWorkout.DoesNotExist:
            return Response('ProgramWorkout does not exist', status=status.HTTP_404_NOT_FOUND)
        
        program = request.data.get('program')
        if (program):
            try:
                programObject = Program.objects.get(pk=program)
            except Program.DoesNotExist:
                return Response('Program does not exist', status=status.HTTP_404_NOT_FOUND)
            programWorkout.program = programObject
        details = request.data.get('details')
        if (details):
            programWorkout.details = details
        programWorkout.save()

        return Response(ProgramWorkoutSerializer(programWorkout).data, status=status.HTTP_200_OK)
    

class ProgramWorkoutDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request:Request, program:int, pk:int) -> Response:
        try:
            programObject = Program.objects.get(pk=program)
        except Program.DoesNotExist:
            return Response('Program does not exist', status=status.HTTP_404_NOT_FOUND)
        try:
            programWorkout = ProgramWorkout.objects.get(program=programObject, pk=pk)
        except ProgramWorkout.DoesNotExist:
            return Response('Workout does not exist or Workout does not belong to the Program', status=status.HTTP_404_NOT_FOUND)
        
        programWorkout.delete()
        return Response('Successfully deleted', status=status.HTTP_204_NO_CONTENT)


class WorkoutsView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request:Request) -> Response:
        response = {}
        response['Push'] = WorkoutSerializer(Workout.objects.filter(type='PS').order_by('name'), many=True).data
        response['Pull'] = WorkoutSerializer(Workout.objects.filter(type='PL').order_by('name'), many=True).data
        response['Lower'] = WorkoutSerializer(Workout.objects.filter(type='L').order_by('name'), many=True).data
        response['Upper'] = WorkoutSerializer(Workout.objects.filter(type='U').order_by('name'), many=True).data
        response['Core'] = WorkoutSerializer(Workout.objects.filter(type='C').order_by('name'), many=True).data
        return Response(response, status=status.HTTP_200_OK)


class ProgramWorkoutRecordsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, programWorkout:int) -> Response:
        try:
            programWorkout = ProgramWorkout.objects.get(pk=programWorkout)
        except ProgramWorkout.DoesNotExist:
            return Response('ProgramWorkout does not exist', status=status.HTTP_404_NOT_FOUND)
        
        records = ProgramWorkoutRecord.objects.filter(programWorkout=programWorkout).order_by('-date')
        return Response(ProgramWorkoutRecordSerializer(records, many=True).data, status=status.HTTP_200_OK)

    def post(self, request:Request, programWorkout:int) -> Response:
        try:
            programWorkout = ProgramWorkout.objects.get(pk=programWorkout)
        except ProgramWorkout.DoesNotExist:
            return Response('ProgramWorkout does not exist', status=status.HTTP_404_NOT_FOUND)

        records = ProgramWorkoutRecord.objects.filter(programWorkout=programWorkout)
        if (len(records) == 10):
            records.first().delete()
        details = request.data.get('details')
        if (not details):
            return Response({'details':'Does not contain details'}, status=status.HTTP_400_BAD_REQUEST)
        record = ProgramWorkoutRecord(programWorkout=programWorkout, details=details)
        record.save()

        return Response({'id':record.pk, 'date':record.date, 'details':record.details}, status=status.HTTP_201_CREATED)


class TimelineRecordsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        records = TimelineRecord.objects.filter(member=member).order_by('-date')
        return Response(TimelineRecordSerializer(records, many=True).data, status=status.HTTP_200_OK)

    def post(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)

        if (not request.data):
            return Response('Does not contain information', status=status.HTTP_400_BAD_REQUEST)
        record = TimelineRecord(member=member, height=request.data.get('height'), weight=request.data.get('weight'))
        img = request.data.get('img')
        if (img):
            record.img.save('image.jpg', ContentFile(base64.b64decode(img)))
        record.save()
        return Response('Successfully Created', status=status.HTTP_201_CREATED)


class CurrentTimelineRecordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request) -> Response:
        try:
            member = Member.objects.get(pk=self.request.user)
        except Member.DoesNotExist:
            return Response('Member does not exist', status=status.HTTP_404_NOT_FOUND)
        
        records = TimelineRecord.objects.filter(member=member).order_by('-date')
        return Response(TimelineRecordSerializer(records.first()).data, status=status.HTTP_200_OK)

