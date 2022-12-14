from django.db.models.signals import pre_save
from django.dispatch import receiver
from cart.models import CartItem, Cart


@receiver(pre_save, sender=Cart)
def handle_pre_save_model_Cart(sender, instance: Cart, **kwargs):
    instance.name = 'Cart ' + str(instance.id)


@receiver(pre_save, sender=CartItem)
def handle_pre_save_model_CartItem(sender, instance: CartItem, **kwargs):
    item = Cart.objects.get(id=instance.cart.id)
    item.total = round(item.total - instance.total, 2)
    instance.total = round(float(instance.quantity) * float(instance.item.price), 2)
    item.total = round(item.total + instance.total, 2)
    item.save()
