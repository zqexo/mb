from django.urls import path
from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import contacts

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),  # Все товары
    path('products/<slug:slug>/', views.ProductListView.as_view(), name='products_by_category'),  # Товары по категории
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path("contacts/", contacts, name="contact"),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

]
