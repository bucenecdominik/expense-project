from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('money_spent_today/', views.money_spent_today, name="money_spent_today"), 
    path('money_spent_this_month/', views.money_spent_this_month, name="money_spent_this_month"),
    path('money_spent_this_year/', views.money_spent_this_year, name="money_spent_this_year"),
    path('delete_item/<item_id>/', views.delete_item, name='delete_item'),
    path('add_item/', views.add_item, name="add_item"),
    
]