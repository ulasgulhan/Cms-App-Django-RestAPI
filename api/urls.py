from django.urls import path
from . import views

urlpatterns = [
    # Authenticate Process
    path('register/', views.registration_view, name='api_register'),
    path('login/', views.login_view, name='api_login'),
    path('logout/', views.logout_view, name='api_logout'),

    # Profile and Dashboard Product CRUD
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('profile/dashboard/', views.DashboardAPIView.as_view(), name='api_dashboard'),
    path('profile/dashboard/create', views.ProductCreateAPIView.as_view(), name='api_create'),
    path('profile/dashboard/update/<int:product_id>', views.ProductUpdateAPIView.as_view(), name='api_update'),
    path('profile/dashboard/delete/<pk>', views.ProductDeleteAPIView.as_view(), name='api_delete'),

    # User Permisson
    path('profile/dashboard/permisson', views.PermissionAPIView.as_view(), name='api_permisson'),
    path('profile/dashboard/permisson/<pk>', views.PermissionChangeAPIView.as_view(), name='api_permisson_change'),

    # Product Read Operations
    path('list/', views.ProductListAPIView.as_view(), name='product_list'),
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('subcategories/', views.SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('<slug:category_slug>/', views.ProductByCategoryListAPIView.as_view(), name='api_product_by_category'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', views.ProductBySubCategoryListAPIView.as_view(), name='product_by_subcategory/'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
]
