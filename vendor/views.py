from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .forms import VendorForm ,OpeningHourForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor, OpeningHour
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import chech_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from django.db.utils import IntegrityError


def get_vendor(request) -> Vendor:
    return Vendor.objects.get(user=request.user)

def custom_slugify(*args: str):
    """Make slug based on args"""
    from functools import reduce
    return  reduce(lambda a, b: str(a) + "-" + str(b), args)

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
            category.slug = custom_slugify(form.cleaned_data['category_name'],get_vendor(request))
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
            category.slug = custom_slugify(form.cleaned_data['category_name'],get_vendor(request))
            form.save()
            messages.success(request, 'Changes has been applied')
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


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def add_fooditem(request):

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['food_title']
            item: FoodItemForm = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = custom_slugify(title,get_vendor(request))
            form.save()
            messages.success(request,f'Product {title} added successfully')
            return redirect('food_items_by_category', item.category.id)
        else: 
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
    }
    return render(request,'vendor/add_fooditem.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def edit_fooditem(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form: FoodItemForm = FoodItemForm(request.POST, request.FILES, instance=item) 
        if form.is_valid():
            item: FoodItemForm = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = custom_slugify(form.cleaned_data['food_title'],get_vendor(request))
            cat_id = item.category.id
            item.save()
            messages.success(request, 'Changes has been applied')
            return redirect('food_items_by_category', pk=cat_id)
    else:
        form = FoodItemForm(instance=item)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'vendor/edit_fooditem.html', context)


@login_required(login_url='login')
@user_passes_test(chech_role_vendor)
def delete_fooditem(request, pk):
    item: FoodItem = get_object_or_404(FoodItem, pk=pk)
    item_name = item.food_title
    item.delete()
    messages.success(request, f'Product {item_name} was deleted')
    return redirect('food_items_by_category', item.category.id) 


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': OpeningHourForm(),
        'opening_hours':opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            try:
                hour = OpeningHour.objects.create(
                    vendor=get_vendor(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed
                   )
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {
                            'status': 'success',
                            'id': hour.id,
                            'day': day.get_day_display(),
                            'is_closed': 'Closed',
                        }
                    else:

                        response = {
                            'status':'success',
                            'id': hour.id,
                            'day': day.get_day_display(),
                            'from_hour': hour.from_hour,
                            'to_hour': hour.to_hour,
                        }
                return JsonResponse(response)
            except IntegrityError:
                response = {
                    'status':'failed',
                    'message':from_hour+'-'+to_hour+' already exists for this day',
                }
                return JsonResponse(response)
        else:
            return HttpResponse('Invalid request')

def remove_opening_hours(request, pk: int = None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            response = {
                'status': 'success',
                'id': pk,
                }
            return JsonResponse(response)

