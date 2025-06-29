from django.urls import path
from dietary import views

urlpatterns = [
    path('meal', views.DietaryMealView.as_view(), name='meal')
]
