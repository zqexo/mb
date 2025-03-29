from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from catalog.models import Category, Product
from django.db.models import Q


from django.views.generic import TemplateView


def contacts(request):
    return render(request, "catalog/contacts.html")


class HomePageView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['user_profile'] = self.request.user
        return context


class CategoryListView(ListView):
    """Список всех категорий."""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    """Список всех товаров или товаров в категории."""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Получаем товары, фильтруя по категории, если указана."""

        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            return Product.objects.filter(category=self.category).order_by('-created_at')
        return Product.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст, если она указана."""
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'category'):
            context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    """Детальная страница товара."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_sizes'] = self.get_object().available_sizes()
        return context


class SearchResultsView(ListView):
    """Поиск товаров."""
    model = Product
    template_name = 'catalog/search_results.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).order_by('-created_at')
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class CategoryDetailView(ListView):
    """Детальная страница категории с отображением товаров."""
    model = Product
    template_name = 'catalog/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Фильтруем товары по категории."""
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Product.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
