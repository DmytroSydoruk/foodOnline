from .models import Vendor
from orders.models import Order, OrderedFood
from menu.models import Category
from django.db.models import Sum


def vendor_statement(request) -> dict:
    """Get statement for specific vendor."""
    vendor: Vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor)
    _number_of_oredered_items: int = OrderedFood.objects.filter(fooditem__vendor=vendor, order__status='Completed').count()

    for category in categories:
        category.income:float = OrderedFood.objects.filter(
            fooditem__category=category, order__status='Completed').aggregate(income=Sum('amount'))['income']
        if category.income == None:
            category.income = 0

        _quantity_of_items_in_category: int = OrderedFood.objects.filter(
            fooditem__category=category, order__status='Completed').count()
        
        _persents: float = 100/_number_of_oredered_items*_quantity_of_items_in_category
        
        category.persents:float = round(_persents,1) if _persents > 0 else 0 

    total_income = OrderedFood.objects.filter(fooditem__vendor=vendor, order__status='Completed').aggregate(total=Sum('amount'))['total']


    context: dict = {
        'vendor': vendor,
        'categories': categories,
        'total_income': total_income,
    }
    return context
