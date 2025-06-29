from rest_framework import serializers
from dietary.models import Meal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'name', 'mealType', 'bodyGoal',
            'calorie', 'protein', 'carb', 'fat'
            ]
