from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tax
from .models import Product
from POS.models import OrderItem

@receiver(post_save, sender=Tax)
def update_services_on_tax_change(sender, instance, **kwargs):

    related_services = Product.objects.filter(tax_value=instance)
    for service in related_services:
        service.save() 


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_totals(sender, instance, **kwargs):
    order = instance.order
    order.update_totals()
    order.calculate_balance()