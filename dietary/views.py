from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from dietary.models import Meal, Category
from dietary.serializers import MealSerializer

# Create your views here.


class DietaryMealView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request:Request) -> Response:
        height = float(request.query_params.get('height'))
        weight = float(request.query_params.get('weight'))
        category = None
        bmi_category = ""
        if (not (height and weight)):
            return Response('Height and weight are required', status=status.HTTP_400_BAD_REQUEST)
        if (height <= 0 or weight <= 0):
            return Response('Height and weight must be positive', status=status.HTTP_400_BAD_REQUEST)

        bmi = weight / (height**2)
        if (bmi < 18.5):
            bmi_category = 'UW'
        elif (bmi < 25):
            bmi_category = 'HW'
        elif (bmi < 30):
            bmi_category = 'OW'
        else:
            bmi_category = 'O'
        categories = Category.objects.filter(bmi=bmi_category)
        meals = []
        for category in categories:
            meal = MealSerializer(category.meal)
            meals.append(meal.data)
        return Response(meals, status=status.HTTP_200_OK)
