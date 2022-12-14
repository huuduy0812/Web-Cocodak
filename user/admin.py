from django.contrib import admin
from user.models import User, Favorite


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'phone', 'address')


class FavoriteAmin(admin.ModelAdmin):
    list_display = ('product_id', 'user_id')


admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAmin)
