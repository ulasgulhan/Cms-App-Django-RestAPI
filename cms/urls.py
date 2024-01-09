from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    # path('category/<slug:category_slug>/<slug:subcategory_slug>', views.sub, name='products_by_subcategory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)