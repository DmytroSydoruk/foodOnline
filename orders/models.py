from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor

# class Payment(models.Model):

#     PAYMENT_METHODS = (
#         ('Cash', 'Cash'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     transaction_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=20 , choices=PAYMENT_METHODS)
#     amount = models.CharField(max_length=100 )
#     status = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __unicode__(self):
#         return self.transaction_id




class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    total_data = models.JSONField(blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    # payment_method = models.CharField(max_length=25)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def restaurants(self):
        return ', '.join([str(i) for i in self.vendors.all()])

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(choices=STATUS,blank=True, null=True, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title