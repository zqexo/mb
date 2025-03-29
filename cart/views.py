import json
import uuid

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from yookassa.domain.exceptions import ApiError

from cart.models import Cart, CartItem
from catalog.models import Product
from django.db.models import F
from django.conf import settings
from yookassa import Configuration, Payment
from django.http import JsonResponse

# Настройка API-ключей
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


@login_required
def create_payment(request):
    """Создание платежа YooKassa и возврат confirmation_token."""
    cart = CartItem.objects.filter(cart__user=request.user)

    if not cart.exists():
        return JsonResponse({'error': 'Корзина пуста'}, status=400)

    total_amount = sum(item.product.price * item.quantity for item in cart)
    unique_order_id = str(uuid.uuid4())  # Уникальный идентификатор заказа

    try:
        payment = Payment.create({
            "amount": {
                "value": f"{total_amount:.2f}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "embedded"  # Виджет оплаты
            },
            "capture": True,
            "description": f"Оплата заказа {unique_order_id}",
            "metadata": {
                "user_id": request.user.id,
                "order_id": unique_order_id
            }
        })
    except ApiError as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'confirmation_token': payment.confirmation.confirmation_token})

@login_required
def payment_callback(request):
    """Обработка успешной оплаты (коллбэк от YooKassa)."""
    event = json.loads(request.body)

    if event.get("event") == "payment.succeeded":
        metadata = event["object"]["metadata"]
        user_id = metadata.get("user_id")

        # Очищаем корзину пользователя
        CartItem.objects.filter(cart__user_id=user_id).delete()

    return JsonResponse({"status": "ok"})


@login_required
def cart_detail(request):
    """Отображение корзины текущего пользователя с оптимизированными запросами."""
    cart, _ = Cart.objects.prefetch_related("items__product").get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    """Добавление товара в корзину."""
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        CartItem.objects.filter(cart=cart, product=product).update(quantity=F('quantity') + 1)

    return JsonResponse({'message': 'Товар добавлен в корзину!'})


@login_required
def remove_from_cart(request, item_id):
    """Удаление товара из корзины."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return JsonResponse({'message': 'Товар удален из корзины!'})


@login_required
def update_cart_item(request, item_id):
    """Обновление количества товара в корзине."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)

    cart_item.quantity = new_quantity
    cart_item.save()

    return JsonResponse({'message': 'Количество обновлено!', 'total_price': cart_item.get_total_price})

