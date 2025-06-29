from rest_framework.serializers import ModelSerializer
from sales.models import Sale



class SaleSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'date', 'amount', 'description', 'receipt_no']
        extra_kwargs = {
            'date':{'read_only':True},
            'id':{'read_only':True},
            }
