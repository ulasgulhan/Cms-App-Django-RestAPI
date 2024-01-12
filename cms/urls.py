from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>', views.store, name='products_by_subcategory'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>', views.product_details, name='product_details'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.remove_cart, name='remove_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)