import random
import secrets
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm
from users.models import User
from MirBelia.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя с отправкой email для подтверждения.
    """
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(16)
        user.save()

        # Отправка email с подтверждением
        confirm_url = f"http://{self.request.get_host()}/users/email-confirm/{user.token}/"
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Добро пожаловать! Подтвердите регистрацию: {confirm_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        messages.success(self.request, "На вашу почту отправлено письмо для подтверждения регистрации.")

        # Обработка AJAX-запросов
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect_url": str(self.success_url)})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})
        return super().form_invalid(form)


def email_verification(request, token):
    """
    Представление для подтверждения email с использованием токена.
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None  # Очистка токена после подтверждения
    user.save()
    return redirect(reverse("users:login"))


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "redirect_url": self.get_success_url()})
        return response


class UserLogoutView(LogoutView, LoginRequiredMixin):
    """
    Представление для выхода пользователя.
    """
    template_name = "users/login.html"
    next_page = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)


from django.core.exceptions import ValidationError
from django.conf import settings


@login_required
def edit_avatar(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        try:
            user = request.user
            avatar = request.FILES["avatar"]

            # Проверка размера файла (например, ограничение в 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if avatar.size > max_size:
                messages.error(request, "Размер файла слишком большой. Максимально допустимый размер — 5MB.")
                return redirect("users:profile")

            user.avatar = avatar
            user.save()
            messages.success(request, "Аватар успешно изменён!")
            return redirect("users:profile")
        except Exception as e:
            # Обработка других ошибок
            messages.error(request, f"Произошла ошибка при изменении аватара: {str(e)}")
            return redirect("users:profile")

    messages.warning(request, "Файл не выбран!")
    return redirect("users:profile")


class PasswordResetView(View, LoginRequiredMixin):
    """
    Представление для сброса пароля.
    """
    form_class = PasswordResetForm
    template_name = "users/password_reset.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                new_password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
                user.password = make_password(new_password)
                user.save()

                send_mail(
                    subject="Восстановление пароля",
                    message=f"Ваш новый пароль: {new_password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[email],
                )
                return redirect(reverse("users:login"))
            except User.DoesNotExist:
                form.add_error("email", "Пользователь с таким email не найден")
        return render(request, self.template_name, {"form": form})


class ProfileView(TemplateView, LoginRequiredMixin):
    """
    Представление для отображения профиля пользователя.
    """
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """
    model = User
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        """Обработка ошибок и отображение пользователю."""
        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)
