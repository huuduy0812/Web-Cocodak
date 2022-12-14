from django import template
from cart.models import Cart, CartItem
from product.models import Category, Product

register = template.library()


@register.simple_tag()
def object_product():
    return Product.objects.all()

@register.simple_tag()
def object_category():
    return Category.objects.all()

