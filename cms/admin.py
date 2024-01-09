from django.contrib import admin
from .models import Category, SubCategory, Product, Pages

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display        = ('category_name', 'status')


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('subcategory_name',)}
    list_display        = ('subcategory_name', 'parent_category', 'status')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display        = ('product_name', 'category', 'status', 'stock', 'price', 'created_date')


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('page_name',)}
    list_display        = ('page_name', 'status', 'created_date', 'modified_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Pages, PageAdmin)
