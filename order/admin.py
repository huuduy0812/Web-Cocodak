from django.contrib import admin
from order.models import Order, Orderitem


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'shipping_address', 'status', 'ship', 'total_all')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(Orderitem, OrderItemAdmin)
