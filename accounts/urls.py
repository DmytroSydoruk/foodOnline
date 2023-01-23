from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('myAccount/', views.myAccount, name='myAccount'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('vendor/',include('vendor.urls')),
    path('customer/', include('customer.urls')),
]
