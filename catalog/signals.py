from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductSize, Product

@receiver(post_save, sender=ProductSize)
@receiver(post_delete, sender=ProductSize)
def update_category_on_product_size_change(sender, instance, **kwargs):
    """Обновляет данные категории при изменении количества размеров продукта."""
    if instance.product.category:
        instance.product.category.update_size_summary()

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def update_category_on_product_change(sender, instance, **kwargs):
    """Обновляет данные категории при изменении продукта."""
    if instance.category:
        instance.category.update_size_summary()
