from django.urls import path
from .views import SalesView

urlpatterns = [
    path('add', SalesView.as_view(), name='sales-list-create'),
]
