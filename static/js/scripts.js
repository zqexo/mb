// Инициализация подсказок Bootstrap
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// Плавная прокрутка до якоря
$(document).ready(function () {
    $("a[href^='#']").on("click", function (e) {
        e.preventDefault();
        $("html, body").animate({
            scrollTop: $($(this).attr("href")).offset().top,
        }, 500);
    });
});

// Уведомление о добавлении в корзину
$(document).on('click', '.btn-add-to-cart', function () {
    alert("Товар успешно добавлен в корзину!");
});

// Анимация появления карточек
$(document).ready(function () {
    $(".card").hide().fadeIn(1000);
});

// Подтверждение удаления через модальное окно
$(document).on('click', '.btn-delete', function (e) {
    e.preventDefault();
    const url = $(this).data('url');
    if (confirm("Вы уверены, что хотите удалить этот товар?")) {
        window.location.href = url;
    }
});
