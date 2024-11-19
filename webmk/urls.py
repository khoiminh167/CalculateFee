from django.contrib import admin
from django.urls import path, include

from . import views
from calculateFee.views import OrderCreateView,order_list,export_to_pdf

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('carts/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),

    path('orders/', include('orders.urls')),
    path('calculatefee/list', order_list, name='order_list'),
    path('export_to_pdf/<int:order_id>/', export_to_pdf, name='export_to_pdf'),

    path('calculatefee/create/', OrderCreateView.as_view(), name='order_create'),

    path('calculatefee/', include('calculateFee.urls',namespace='calculateFee')),  # Include URLs from the calculateFee app

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)