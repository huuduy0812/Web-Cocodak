from django.contrib import admin
from cart.models import Cart, CartItem


# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'quantity', 'total')


class CartAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_at', 'update_at', 'total')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
