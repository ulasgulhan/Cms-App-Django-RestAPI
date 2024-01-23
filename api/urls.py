from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
    path('list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('subcategories/', views.SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('<slug:category_slug>/', views.ProductByCategoryListAPIView.as_view(), name='product_by_category'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.ProductBySubCategoryListAPIView.as_view(), name='product_by_subcategory/'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.ProductDetailAPIView.as_view(), name='product_detail'),
]
