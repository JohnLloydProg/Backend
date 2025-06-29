from django.db import models

# Create your models here.


class Sale(models.Model):
    date = models.DateField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    receipt_no = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.description}"
