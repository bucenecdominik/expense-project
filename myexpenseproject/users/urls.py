from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login_user/', views.LoginView.as_view(), name='login'),
    path('logout_user/', views.LogoutView.as_view(), name='logout'),
    path('register_user/', views.RegisterView.as_view(), name='register_user'),
    path('money_spent/', views.MoneySpentView.as_view(), name='money_spent'),
    path('<int:id>/', views.ItemDetailView.as_view(), name='detail'),
    path('standing_orders/', views.StandingOrderView.as_view(), name='standing_order'),
    path('delete_item/<item_id>', views.ItemDeleteView.as_view(), name='delete_item'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<id>/update', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<id>/delete', views.StandingOrderDeleteView.as_view(), name='delete_order'),
    path('<id>/update', views.StandingOrderUpdateView.as_view(), name='update_order'),
    path('report', views.ReportGenerationView.as_view(), name='report'),
]