from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import SaleSerializer
from .models import Sale
from django.utils.timezone import now
from rest_framework import status

# Create your views here.

class SalesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request:Request) -> Response:
        amount = request.data.get('amount')
        description = request.data.get('description')
        receipt_no = request.data.get('receipt_no')
        if (not amount):
            return Response('Missing amount', status=status.HTTP_400_BAD_REQUEST)
        sale = Sale(amount=amount, description=description, receipt_no=receipt_no)
        sale.save()
        return Response(SaleSerializer(sale).data, status=status.HTTP_201_CREATED)
