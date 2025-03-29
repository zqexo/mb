from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Регистрируем модель пользователя
class CustomUserAdmin(UserAdmin):
    model = User
    # Указываем поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'is_staff', 'is_active')
    # Указываем поля, которые будут фильтроваться
    list_filter = ('is_staff', 'is_active', 'date_joined')
    # Указываем, какие поля должны быть доступны для поиска
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    # Указываем, какие поля показывать на странице редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личное', {'fields': ('first_name', 'last_name', 'phone', 'avatar', 'token')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    # Определяем, какие поля можно редактировать
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'avatar')}
        ),
    )
    # Сортировка
    ordering = ('email',)

# Регистрируем модель с использованием кастомного администратора
admin.site.register(User, CustomUserAdmin)
