from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime


class Item(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    time_it_was_bought = models.DateTimeField(default= datetime.now())
    price = models.IntegerField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    budget = models.IntegerField(default=1)
    bio = models.TextField()
    

    def __str__(self):
        return str(self.user)

    
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



