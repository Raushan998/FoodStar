from django.db import models 
from myapp.models.product import Product
from myapp.models.Users import User
import datetime

class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    payment_request_id=models.CharField(max_length=200,default=0)
    payment_id=models.CharField(max_length=200,default=0)
    status=models.BooleanField(default=False)
    date=models.DateField(default=datetime.datetime.today)
    