import re

from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    Форма для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserProfileForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()  # Скрытие поля пароля

        # Кастомизация виджетов
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields["phone"].widget.attrs["placeholder"] = "Введите номер телефона"
        self.fields["email"].widget.attrs["placeholder"] = "Введите ваш email"
        self.fields["first_name"].widget.attrs["placeholder"] = "Ваше имя"
        self.fields["last_name"].widget.attrs["placeholder"] = "Ваша фамилия"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email не может быть пустым.")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Этот email уже используется.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            raise ValidationError("Телефон не может быть пустым.")

        phone = phone.strip().replace(" ", "")

        if phone.startswith("+7"):
            phone = "8" + phone[2:]  # Заменяем +7 на 8

        phone = re.sub(r"\D", "", phone)  # Удаляем все символы, кроме цифр

        if not phone.isdigit():
            raise ValidationError("Телефон должен содержать только цифры.")
        if len(phone) < 10 or len(phone) > 15:
            raise ValidationError("Телефон должен содержать от 10 до 15 цифр.")

        return phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("Имя не может быть пустым.")
        if len(first_name) < 2:
            raise ValidationError("Имя должно содержать хотя бы 2 символа.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Фамилия не может быть пустой.")
        if len(last_name) < 2:
            raise ValidationError("Фамилия должна содержать хотя бы 2 символа.")
        return last_name


class UserLoginForm(AuthenticationForm):
    """
    Форма для входа пользователя.
    """
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
