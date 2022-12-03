from datetime import datetime
from .models import Item, StandingOrder

def get_sum_items(user, date):
    items = Item.objects.filter(user=user, time_it_was_bought__month = date)
    sum_items =  sum(item.price for item in items)
    return sum_items

def get_sum_orders(user):
    standing_orders = StandingOrder.objects.filter(user=user)
    sum_standing_orders =  sum(order.price for order in standing_orders)
    return sum_standing_orders

def get_budget(user, date):
    budget = user.profile.monthly_income
    items = Item.objects.filter(user=user, time_it_was_bought__month = date)
    standing_orders = StandingOrder.objects.filter(user = user)
    sum_items = sum(item.price for item in items)
    sum_orders = sum(order.price for order in standing_orders)
    final_budget = budget - (sum_items + sum_orders)
    return final_budget

def get_month():
    month = datetime.now().strftime("%B")
    return month