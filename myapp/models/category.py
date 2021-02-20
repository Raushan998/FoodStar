from django.db import models

class Cateogary(models.Model):
    FoodType=models.CharField(max_length=100);

    def __str__(self):
        return self.FoodType

class Location(models.Model):
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.location