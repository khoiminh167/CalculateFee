# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import OrderCreateView,MainOrderCreateView,OrderDetailView,export_to_pdf
app_name = 'calculateFee'

urlpatterns = [
    path('drinkorder/', views.order_list, name='order_list'),
    path('create_order_detail/', OrderCreateView.as_view(), name='create_order_detail'),
    path('create_order/', MainOrderCreateView.as_view(), name='create_order'),
    path('view/<int:pk>/', OrderDetailView.as_view(), name='order_view'),
    path('create_order_detail/<int:order_id>/', OrderCreateView.as_view(), name='create_order_detail'),
   path('export_to_pdf/<int:order_id>/', export_to_pdf, name='export_to_pdf'),


    # Other URL patterns
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)