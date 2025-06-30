from rest_framework import serializers
from gym.models import Program, ProgramWorkout, Workout, ProgramWorkoutRecord, TimelineRecord


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'day', 'member']
        extra_kwargs = {'member':{'read_only':True}}


class ProgramWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramWorkout
        fields = ['id', 'workout', 'details']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'type', 'time', 'sets', 'reps', 'weight', 'distance']


class ProgramWorkoutRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramWorkoutRecord
        fields = ['id', 'date', 'details']
        extra_kwargs = {'date':{'read_only':True}}


class TimelineRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineRecord
        fields = ['id', 'date', 'height', 'weight', 'img', 'notes']