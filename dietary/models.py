from django.db import models

# Create your models here.


class Meal(models.Model):
    name = models.CharField(max_length=100)
    mealType = models.CharField(max_length=5, choices={'BF':'Breakfast', 'L':'Lunch', 'D':'Dinner', 'S':'Snacks'})
    bodyGoal = models.CharField(max_length=100)
    calorie = models.FloatField()
    protein = models.FloatField()
    carb = models.FloatField()
    fat = models.FloatField()


class Category(models.Model):
    bmi = models.CharField(max_length=15, choices={
        'UW':'Under Weight', 'HW':'Healthy Weight',
        'OW':'Over Weight', 'O':'Obese'
    })
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
