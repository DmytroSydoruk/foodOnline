from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
from .context_processors import get_cart_counter ,get_cart_amount
from django.contrib.auth.decorators import login_required


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True)
    categories = Category.objects.all()
    for vendor in vendors:
        vendor.categories: list = []
        for category in categories:
            if category.vendor == vendor:
                vendor.categories.append(category)

    paginator = Paginator(vendors, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'marketplace/listing.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

    else: 
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 
                                        'message': 'increase card quantity', 
                                        'cart_counter': get_cart_counter(request),
                                        'qty': chkCart.quantity,
                                        'cart_amount': get_cart_amount(request),
                                        'price': fooditem.price,})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 
                                        'message': 'Food added to the cart', 
                                        'cart_counter': get_cart_counter(request),
                                        'qty': chkCart.quantity,
                                        'cart_amount': get_cart_amount(request),
                                        'price': fooditem.price,})
            except:
                return JsonResponse({'status': 'Failed', 
                                    'message': 'This food does not exist'})
        # return JsonResponse({'status': 'Success', 'message': 'user is logged in'})
        else:
            return JsonResponse({'status': 'Failed', 
                                'message': 'Invalid request'})

    else:
        return JsonResponse({'status': 'login_required', 
                            'message': 'Login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        # fi request is ajax
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if food exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:  
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success',
                                        'cart_counter': get_cart_counter(request),
                                        'qty': chkCart.quantity,
                                        'cart_amount': get_cart_amount(request),
                                        'price': fooditem.price,})
                except:
                    return JsonResponse({'status': 'Failed',
                                        'message': 'You dont have this food in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 
                                    'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 
                                'message': 'Invalid request'})

    else:
        return JsonResponse({'status': 'login_required', 
                            'message': 'Login to continue'})


@login_required(login_url = 'login')
def cart(request):
    cart_items: Cart = Cart.objects.filter(user=request.user).order_by('created_at')
    for item in cart_items:
        item.price = item.fooditem.price * item.quantity

    context = {
        'cart_items': cart_items,
    }
    return render(request,'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        # if ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.filter(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success',
                        'message': 'Cart item has been deleted',
                        'cart_counter':get_cart_counter(request),
                        })
            except:
                return JsonResponse({
                    'status': 'Failed', 
                    'message': 'Cart item does not exist',
                    })
        else:
            return JsonResponse({
                'status': 'Failed', 
                'message': 'Invalid request',
                })

