from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.cart, name='cart'),
    path('<int:product_id>', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>', views.remove_cart, name='remove_cart'),
    path('discard/<int:product_id>', views.discard_cart_item, name='discard_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)