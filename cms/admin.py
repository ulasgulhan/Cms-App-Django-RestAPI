from django.contrib import admin



from .models import Cart, CartItem, Category, SubCategory, Product, Pages, Variations

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display        = ('category_name', 'status')
    list_editable       = ('status',)



class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('subcategory_name',)}
    list_display        = ('subcategory_name', 'parent_category', 'status')
    list_editable       = ('status',)



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display        = ('product_name', 'category', 'status', 'stock', 'price', 'created_date')
    list_editable       = ('status',)




class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('page_name',)}
    list_display        = ('page_name', 'status', 'created_date', 'modified_date')


class VariationAdmin(admin.ModelAdmin):
    list_display        = ('product_name', 'variation_category', 'variation_value', 'status')
    list_editable       = ('status',)


class CartAdmin(admin.ModelAdmin):
    list_display        = ('user',)


class CartItemAdmin(admin.ModelAdmin):
    list_display        = ('product', 'cart', 'quantity', 'status')

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Pages, PageAdmin)
admin.site.register(Variations, VariationAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
