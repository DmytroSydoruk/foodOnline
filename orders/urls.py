from django.urls import path, include
from . import views

urlpatterns = [
    path("place-order/", views.place_order, name='place_order'),
    path('cofirm_order/', views.confirm_order , name='confirm_order1'),
]
