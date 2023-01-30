from django.shortcuts import render, redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amount
from .forms import OrderForm
from .models import Order, OrderedFood
from .utils import generate_order_number
from django.http import HttpResponse
from accounts.utils import send_notification ,send_notification_to_vendors
from django.contrib.auth.decorators import login_required
from django.contrib import messages


login_required(login_url='login')
def place_order(request):
    total = get_cart_amount(request)['total']

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order. pin_code = form.cleaned_data['pin_code']

            order.user = request.user
            order.total = total

            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()

            context = {
                'cart_items': Cart.objects.filter(user=request.user),
                'order': order,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)

    return render(request, 'orders/place_order.html')


login_required(login_url='login')
def confirm_order(request, order_number):
    # change status
    order = Order.objects.get(user=request.user, order_number=order_number)
    order.is_ordered = True
    order.save()
    # add fooitems to ordered food
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        ordered_food: OrderedFood = OrderedFood()
        ordered_food.user = request.user    
        ordered_food.order = order
        ordered_food.fooditem = item.fooditem
        ordered_food.quantity = item.quantity
        ordered_food.price = item.fooditem.price
        ordered_food.amount = item.fooditem.price * item.quantity
        ordered_food.save()

    # send email to customer
    email_subject = "Thank you for your order!"
    email_template = 'order_confirmation_email.html'
    email_template = 'order_confirmation_email.html'
    context = {
        'user': order,
        'order': order,
    }
    send_notification(email_subject,email_template,context)
    # send email to vendors
    email_subject = 'You have new order'
    email_template = 'new_order_received.html'
    vendors_email = []
    for item in cart_items:
        if item.fooditem.vendor.user.email not in vendors_email:
            vendors_email.append(item.fooditem.vendor.user.email)

    context = {
        'vendors_emails': vendors_email,
        'order': order,
    }
    send_notification_to_vendors(email_subject,email_template,context)

    # Clear cart
    cart_items.delete()

    messages.success(request,'Your order was successfuly created')
    return redirect('myAccount')
