from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='c_profile'),
    path('change-password/', views.cust_change_password , name='cust_change_password'),
    path('orders/', views.customer_orders, name='customer_orders'),
    path('order-details/<int:order_number>/', views.order_detail, name='cust_order_detail')
]
