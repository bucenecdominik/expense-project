from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime


class Item(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    time_it_was_bought = models.DateTimeField(default= datetime.now())
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

    @property
    def calculate_budget(self):
        income = self.monthly_income
        items = Item.objects.filter(time_it_was_bought__month = datetime.now().month)
        prices = sum(item.price for item in items)
        orders = StandingOrder.objects.all()
        order_prices = sum(order.price for order in orders)
        budget = income - (prices + order_prices) 
        return budget
        

    



