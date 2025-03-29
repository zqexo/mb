from django.http import HttpResponseForbidden


class SuperuserPermission:
    """Проверка прав суперпользователя."""

    @staticmethod
    def has_permission(user):
        """Проверка, что пользователь является суперпользователем."""
        return user.is_superuser

    def __call__(self, request):
        """Вызывается для проверки прав перед выполнением вьюшки."""
        if not self.has_permission(request.user):
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return None
