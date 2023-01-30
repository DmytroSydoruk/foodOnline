from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import chech_role_customer
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import UserProfileForm, UserEditForm
from accounts.models import UserProfile, User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from orders.models import Order, OrderedFood


@login_required(login_url='login')
@user_passes_test(chech_role_customer)
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    user = profile.user

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        user_form = UserEditForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            user_form.save()

            messages.success(request, 'Profile data is updated')
            return redirect('c_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserEditForm(instance=user)

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'user': user,
        'user_form': user_form,
    }
    return render(request, 'customer/cprofile.html', context)


def cust_change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user = User.objects.get(pk=request.user.pk)
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('cust_change_password')

        else:
            messages.error(request, 'Passwords does not match')
            return redirect('cust_change_password')
    else:
        context = {
            'profile': UserProfile.objects.get(user=request.user)
        }
        return render(request, 'customer/change_password.html', context)


def customer_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'profile': UserProfile.objects.get(user=request.user),
        'orders': orders,
    }

    return render(request, 'customer/orders.html', context)


def order_detail(request, order_number):
    order = Order.objects.get(order_number=order_number)
    ordered_products = OrderedFood.objects.filter(user=request.user,order=order)
    context = {
        'profile': UserProfile.objects.get(user=request.user),
        'order': order,
        'ordered_products': ordered_products,

    }
    return render(request, 'customer/order_detail.html', context)
