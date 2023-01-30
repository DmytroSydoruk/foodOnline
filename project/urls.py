from django.contrib import admin
from django.urls import path, include
from . import views
from marketplace.views import cart, search, checkout, search_by_city

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    # cart
    path('cart/', cart, name='cart'),
    # search
    path('search/', search, name='search'),
    path('search-by-city/<str:city>', search_by_city, name='search_by_city'),
    # check out
    path('checkout/', checkout, name='checkout'),
    
    path('order/', include('orders.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
