from django.urls import path
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    # sidebar
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('orders/', views.orders, name='vendor_orders'),
    path('order-detail/<int:order_number>',
         views.order_detail, name='vendor_order_detail'),
    path('change-password/', views.change_password, name='ven_change_password'),

    # order features
    path('accept-ordered-food/',
         views.accept_ordered_food, name='accept_ordered_food'),
    path('decline-ordered-food/',
         views.decline_ordered_food, name='decline_ordered_food'),
    path('change-status/', views.change_status, name='change_status'),



    # category crud
    path('menu-builder/category/<int:pk>/',
         views.food_items_by_category, name='food_items_by_category'),
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>',
         views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>',
         views.delete_category, name='delete_category'),

    # fooditem crud
    path('menu-builder/fooditem/add/', views.add_fooditem, name='add_fooditem'),
    path('menu-builder/fooditem/edit/<int:pk>',
         views.edit_fooditem, name='edit_fooditem'),
    path('menu-builder/fooditem/delete/<int:pk>',
         views.delete_fooditem, name='delete_fooditem'),

    # opening hour crud
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/',
         views.remove_opening_hours, name='remove_opening_hours'),
]
