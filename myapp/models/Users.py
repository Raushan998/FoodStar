from django.db import models

class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100,blank=True)
    email=models.CharField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

    def isExists(self):
        if User.objects.filter(email=self.email):
            return True
        else:
            return False

    def __str__(self):
        return self.first_name
    
