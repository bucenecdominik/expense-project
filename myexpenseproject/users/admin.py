from django.contrib import admin
from .models import Item, Profile, StandingOrder

# Register your models here.
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(StandingOrder)