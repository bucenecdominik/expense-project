from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime


class Item(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    time_it_was_bought = models.DateTimeField(default=datetime.now())
    price = models.IntegerField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
   
class StandingOrder(models.Model):
    class Type(models.TextChoices):
        important = "IMPORTANT"
        less_important = "LESS IMPORTANT"
        not_important = "NOT IMPORTANT"

    name = models.CharField(max_length=25)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=25, choices=Type.choices, default=Type.important)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    monthly_income = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    price = models.PositiveIntegerField()
    description = models.TextField()
    photo = models.ImageField()

    def __str__(self):
        return self.name 

    

    

    

        

    



