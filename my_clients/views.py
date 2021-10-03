from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from my_clients.forms import LoginUserForm


class LoginUser(LoginView):
    """
    Отображение формы для авторизации

    При успешной авторизации перенаправляет на главную страницу
    """

    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """
    Выполняет выход пользователя

    После чего перенаправляет на главную страницу
    """

    logout(request)
    return redirect('home')
