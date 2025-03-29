from django import forms
from .models import Category, Product


class CategoryForm(forms.ModelForm):
    """Форма для добавления/редактирования категории."""

    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ProductForm(forms.ModelForm):
    """Форма для добавления/редактирования продукта."""

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }