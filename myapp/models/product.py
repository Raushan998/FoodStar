from django.db import models
from .category import Cateogary,Location

class Product(models.Model):
    cateogary=models.ForeignKey(Cateogary,on_delete=models.CASCADE)
    location=models.ForeignKey(Location,on_delete='DONOTHING',default=True)
    name=models.CharField(max_length=200)
    price=models.IntegerField(default=0)
    discount_price=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to='uploads/files')
    description=models.CharField(max_length=200)

    def __str__(self):
        return self.name;

