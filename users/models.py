from django.contrib.auth.models import AbstractUser
from django.db import models

from MirBelia.settings import DEFAULT_AVATAR_PATH


class User(AbstractUser):
    """
    Модель пользователя с дополнительными полями.
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите ваш адрес электронной почты"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона в международном формате"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение для вашего профиля",
        default=DEFAULT_AVATAR_PATH
    )
    token = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Токен авторизации",
        help_text="Токен используется для двойной аутентификации"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"