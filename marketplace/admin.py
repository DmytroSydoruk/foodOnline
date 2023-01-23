from django.contrib import admin
from .models import Cart, Order


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'fooditem', 'quantity', 'updated_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor', "fooditem", 'quantity','status', ]


admin.site.register(Cart, CartAdmin)
admin.site.register(Order)
