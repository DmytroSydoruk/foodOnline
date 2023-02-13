from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order, OrderedFood
from .utils import generate_order_number
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vendor.models import Vendor
from marketplace.models import Cart

from django.db.models import Sum, F

from project.tasks import send_email
from django.template.loader import render_to_string


@login_required(login_url='login')
def place_order(request):
    vendors = []
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.fooditem.vendor.id not in vendors:
            vendors.append(item.fooditem.vendor.id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            orders_numbers: list = []
            for vendor in vendors:
                order = Order()
                order.first_name = form.cleaned_data['first_name']
                order.last_name = form.cleaned_data['last_name']
                order.phone = form.cleaned_data['phone']
                order.email = form.cleaned_data['email']
                order.address = form.cleaned_data['address']
                order.country = form.cleaned_data['country']
                order.state = form.cleaned_data['state']
                order.city = form.cleaned_data['city']
                order.pin_code = form.cleaned_data['pin_code']
                order.vendor = Vendor.objects.get(pk=vendor)
                order.user = request.user
                order.total = Cart.objects.filter(fooditem__vendor_id=vendor, user=request.user).aggregate(
                    total=Sum(F('fooditem__price') * F('quantity')))['total']
                order.save()
                order.order_number = generate_order_number(order.id)
                order.save()
                orders_numbers.append(order.order_number)

            request.session['orders_numbers'] = orders_numbers
            
            context = {
                'cart_items': Cart.objects.filter(user=request.user),
                'order': order,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)

    return render(request, 'orders/place_order.html')


@login_required(login_url='login')
def confirm_order(request):
    # change status
    orders = Order.objects.filter(
        user=request.user, order_number__in=request.session['orders_numbers'])
    for order in orders:
        order.is_ordered = True
        order.save()
    # add fooitems to ordered food
    cart_items = Cart.objects.filter(user=request.user)
    for order in orders:
        for cart_item in cart_items:
            if cart_item.fooditem.vendor == order.vendor:
                ordered_food: OrderedFood = OrderedFood()
                ordered_food.user = request.user
                ordered_food.order = order
                ordered_food.fooditem = cart_item.fooditem
                ordered_food.quantity = cart_item.quantity
                ordered_food.price = cart_item.fooditem.price
                ordered_food.amount = cart_item.fooditem.price * cart_item.quantity
                ordered_food.status = "New"
                ordered_food.save()
            else:
                continue

    # send email to customer
    try:
        for order in orders:
            email_subject = "Thank you for your order!"
            email_template = 'accounts/emails/order_confirmation_email.html'
            ordered_food = OrderedFood.objects.filter(order=order)
            context = {
                'user': order,
                'order': order,
                'ordered_food':ordered_food,
            }

            email_body = render_to_string(email_template, context)
            user_email: str = order.email

            send_email.delay(email_subject, email_body,user_email,)

    except Exception as e:
        print(f'Exception: send customer email error {e}')

    # send email to vendors
    try:
        for order in orders:
            email_subject = 'You have new order'
            email_template = 'new_order_received.html'
            context = {
                'vendors_emails': order.vendor.user,
                'order': order,
            }
             
            email_body = render_to_string(email_template, context)
            user_email: str = order.email

            send_email.delay(email_subject, email_body,user_email,)

    except Exception as e:
        print(f'Exception: send vendors email error {e}')


    # Clear cart
    cart_items.delete()

    messages.success(request, 'Your order was successfuly created')
    return redirect('myAccount')
