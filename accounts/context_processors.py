from vendor.models import Vendor
from django.conf import settings


def get_vendor(request):
    try:
        vendor: Vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_api_key(request):
    return dict(MAPTILER_API_KEY=settings.MAPTILER_API_KEY)