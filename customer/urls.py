from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='c_profile'),
    path('change-password/', views.cust_change_password , name='cust_change_password'),
    path('orders/', views.customer_orders, name='customer_orders'),
]
