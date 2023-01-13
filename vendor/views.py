from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import chech_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify


def get_vendor(request) -> Vendor:
    return Vendor.objects.get(user=request.user)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def menu_builder(request):
    categories = Category.objects.filter(
        vendor=get_vendor(request)).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def food_items_by_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(
        vendor=get_vendor(request), category=category)
    context = {
        'fooditems': fooditems,
        'category': category,
    }
    return render(request, 'vendor/food_items_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form: CategoryForm = CategoryForm(request.POST)
        if form.is_valid():
            category: CategoryForm = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(form.cleaned_data['category_name'])
            form.save()
            messages.success(request, 'Successfully added!')
            return redirect('menu_builder')
        else:
            pass
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form: CategoryForm = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category: CategoryForm = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(form.cleaned_data['category_name'])
            form.save()
            messages.success(request, 'Changes applied')
            return redirect('menu_builder')
        else:
            pass
    else:
        form = CategoryForm(instance=category)
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'vendor/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def delete_category(request, pk):
    category: Category = get_object_or_404(Category, pk=pk)
    cat_name = category.category_name
    category.delete()
    messages.success(request, f'Category {cat_name} was deleted')
    return redirect('menu_builder')
