from django.db import models
import os
from django.core.validators import MinLengthValidator

# Create your models here.
class credent(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20,primary_key=True)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
    class Meta:
        db_table = 'credentials'

class portfolio(models.Model):
    stock_name = models.CharField(max_length=100)
    phone_number = models.ForeignKey(credent, on_delete=models.CASCADE, db_column='phone_number')
    bought_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    current_price= models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'portfolio'

class balance(models.Model):
    phone_number = models.ForeignKey(credent, on_delete=models.CASCADE, db_column='phone_number')
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=500000.00)

    class Meta:
        db_table = 'balance'