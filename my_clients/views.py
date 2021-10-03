from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView

from my_clients.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    """
    Отображение формы для авторизации

    При успешной авторизации перенаправляет на главную страницу
    """

    form_class = LoginUserForm
    template_name = 'my_clients/login.html'


class RegisterUser(CreateView):
    """Отображение формы регистрации"""
    form_class = RegisterUserForm
    template_name = 'my_clients/sign_up.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)


def logout_user(request):
    """
    Выполняет выход пользователя

    После чего перенаправляет на главную страницу
    """

    logout(request)
    return redirect('home')
