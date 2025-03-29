from django.urls import path
from cart import views
from cart.apps import CartConfig

app_name = CartConfig.name


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/create-payment/', views.create_payment, name='create_payment'),
    path('cart/payment-callback/', views.payment_callback, name='payment_callback')
]
