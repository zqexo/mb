from cart.models import Cart

def cart_context(request):
    cart_item_count = 0  # Изначально количество товаров в корзине 0
    cart_is_empty = True  # По умолчанию считаем, что корзина пуста

    if request.user.is_authenticated:  # Проверяем, авторизован ли пользователь
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item_count = cart.get_total_quantity()  # Получаем количество товаров
            if cart_item_count > 0:
                cart_is_empty = False  # Если товары есть, корзина не пуста
        except Cart.DoesNotExist:
            cart_item_count = 0  # Если корзина не найдена, то товаров 0

    return {'cart_is_empty': cart_is_empty}
