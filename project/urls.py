from django.contrib import admin
from django.urls import path, include
from . import views
from marketplace.views import cart, search, confirm_order

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    # order
    path('cart/', cart, name='cart'),
    path('confirm-order/', confirm_order, name='confirm-order'),
    # path('order/', order, name='order'),
    # search
    path('search/', search, name='search'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
