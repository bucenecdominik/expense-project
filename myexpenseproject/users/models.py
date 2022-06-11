from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    time_it_was_bought = models.DateTimeField()
    price = models.IntegerField()
    