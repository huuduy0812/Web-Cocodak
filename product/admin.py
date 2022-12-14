from django.contrib import admin
from product.models import Category, Product
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'active', 'create_at', 'update_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
