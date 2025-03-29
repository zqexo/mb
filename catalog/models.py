from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Слаг", db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    total_sizes = models.PositiveIntegerField(default=0, verbose_name="Общее количество размеров", editable=False)
    size_list = models.TextField(blank=True, verbose_name="Список размеров", editable=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [models.Index(fields=["slug"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Категория: {self.name}"

    def get_absolute_url(self):
        return reverse("catalog:category_detail", kwargs={"slug": self.slug})

    def update_size_summary(self):
        """Обновляет общее количество и список размеров в категории."""
        sizes = (
            ProductSize.objects.filter(product__category=self)
            .values("size__name")
            .annotate(total=models.Sum("quantity"))
        )
        self.total_sizes = sum(size["total"] for size in sizes)
        self.size_list = ", ".join(f"{size['size__name']} ({size['total']} шт.)" for size in sizes)
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Слаг", db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    seria = models.CharField(max_length=30, blank=True, null=True, verbose_name="Серия или номер продукта", default='Не обозначен')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Продукт: {self.name} - {self.price} ₽"

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def available_sizes(self):
        """Возвращает размеры с количеством больше 0."""
        return self.product_sizes.filter(quantity__gt=0)


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Размер")
    categories = models.ManyToManyField(
        Category,
        related_name="sizes",
        verbose_name="Категории",
        blank=True,
    )

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        categories = ", ".join(category.name for category in self.categories.all())
        return f"{self.name} ({categories})"


class ProductSize(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_sizes", verbose_name="Продукт", null=True, blank=True
    )
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, related_name="product_sizes", verbose_name="Размер", null=True, blank=True
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")

    class Meta:
        verbose_name = "Размер продукта"
        verbose_name_plural = "Размеры продуктов"
        unique_together = ("product", "size")

    def __str__(self):
        return f"{self.product.name} - {self.size.name} ({self.quantity} шт.)"
