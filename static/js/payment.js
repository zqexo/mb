document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-button");
    const paymentForm = document.getElementById("payment-form");
    const storedToken = localStorage.getItem("confirmation_token");
    const storedTimestamp = localStorage.getItem("payment_timestamp");
    const expirationTime = 10 * 60 * 1000; // 10 минут в миллисекундах
    const currentTime = new Date().getTime();

    function renderPaymentForm(token) {
        const checkout = new window.YooMoneyCheckoutWidget({
            confirmation_token: token,
            return_url: 'http://127.0.0.1:8000/cart/',
            error_callback: function (error) {
                console.error("Ошибка:", error);
                localStorage.removeItem("confirmation_token");
                localStorage.removeItem("payment_timestamp");
                payButton.disabled = false;
            }
        });

        checkout.render("payment-form");
        payButton.disabled = true;
    }

    if (storedToken && storedTimestamp && (currentTime - storedTimestamp < expirationTime)) {
        renderPaymentForm(storedToken);
    } else {
        localStorage.removeItem("confirmation_token");
        localStorage.removeItem("payment_timestamp");
    }

    payButton.addEventListener("click", function () {
        if (payButton.disabled) return;

        payButton.disabled = true;
        payButton.innerText = "Обрабатывается...";

        fetch(paymentUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.confirmation_token) {
                localStorage.setItem("confirmation_token", data.confirmation_token);
                localStorage.setItem("payment_timestamp", new Date().getTime());
                renderPaymentForm(data.confirmation_token);
            } else {
                alert("Ошибка при создании платежа!");
                payButton.disabled = false;
                payButton.innerText = "Оплатить";
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
            payButton.disabled = false;
            payButton.innerText = "Оплатить";
        });
    });
});
