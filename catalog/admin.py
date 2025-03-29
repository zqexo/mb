from django.contrib import admin
from .models import Product, Category, ProductSize, Size


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Количество пустых строк для добавления новых записей
    min_num = 0  # Минимальное количество записей
    verbose_name = "Размер продукта"
    verbose_name_plural = "Размеры продукта"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('category', 'price', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {"slug": ("name",)}  # автогенерация slug на основе имени
    ordering = ('-created_at',)
    inlines = [ProductSizeInline]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображаем только название в списке
    search_fields = ('name',)  # Поиск по названию размера
    filter_horizontal = ('categories',)  # Удобный выбор нескольких категорий


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity')  # Поля для отображения
    search_fields = ('product__name', 'size__name')  # Поиск по продукту и размеру
    list_filter = ('size', 'product__category')  # Фильтры по размерам и категориям
    ordering = ('product', 'size')  # Сортировка
