from django.contrib import admin
from .models import Order, OrderedFood


class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ['order','user', 'fooditem', 'quantity', 'price', 'amount']
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name',
                    'phone', 'email', 'total', 'is_ordered']
    inlines = [OrderedFoodInline]


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)
