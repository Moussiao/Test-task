from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, F
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.defaultfilters import date, time
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from strange_posts.forms import LoginUserForm
from strange_posts.models import Post, User
from strange_posts.utils import get_db_filter_based_on_search_query


class StrangePostsHome(ListView):
    """
    Возвращает список постов, разделенных по страницам (постраничная навигация, пагинация).
    Количество постов на странице указана в атрибуте paginate_by.

    Если HTTP GET содержит заданные параметр с ключом 'order_by',
    то мы сортируем посты по определенному значению
    """
    model = Post
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}  # Статическая информация для шаблона

    paginate_by = 10  # Количество записей на странице

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формируем и возвращаем информацию, которую передаем в шаблон"""
        context = super().get_context_data(**kwargs)  # Получаем context у предка
        context['search'] = self.request.GET.get('search')

        return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        sort = self.request.GET.get('order_by')
        cat = self.request.GET.get('cat')
        queryset = Post.objects.select_related('user')

        if search:
            db_filter = get_db_filter_based_on_search_query(search)
            if db_filter is not None:
                queryset = queryset.filter(db_filter)

        if sort:
            queryset = queryset.order_by(sort)

        if cat:
            queryset = queryset.filter(categories__slug=cat)

        return queryset


class GetUser(LoginRequiredMixin, DetailView):
    """Информация о пользователе. Доступно только авторизированным пользователям"""
    model = User
    context_object_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формируем и возвращаем информацию, которую передаем в шаблон"""
        context = super().get_context_data(**kwargs)  # Получаем context у предка
        context['title'] = context['user']

        context['show_data'] = {
            'ID': context['user'].pk,
            'Username': context['user'].username,
            'Имя': context['user'].name,
            'Номер телефона': context['user'].phone_number,
            'Адрес': context['user'].user_address,
            'Email': context['user'].email
        }

        # Последние 8 постов пользователя, сортированных по дате создания, от новых к более поздним
        context['posts'] = Post.objects.filter(user_id=self.kwargs['pk']).order_by('-created_at')[:8]

        return context

    def get_queryset(self):
        return User.objects.annotate(Count('post')).select_related('user_address', 'user_company')


class UserPostsDynamicLoad(View):
    """
    Класс представления для динамической загрузки постов пользователя.

    Связан с кнопкой на странице с информацией о пользователе.
    При нажатии на кнопку посылается GET запрос с информацией о уже загруженных постах и об id пользователя
    """

    @staticmethod
    def get(request, *args, **kwargs):
        """
        Принимает GET запрос и возвращает сформированный ответ в зависимости от считанной информации.

        Сначала мы считываем полученные данные, после чего получаем список еще не загруженных постов.
        Если список не пуст, то возвращаем данные о полученных постах
        Если список пуст, то возвращаем False.
        """
        how_much_to_load = 8
        len_posts = int(request.GET.get('lenPosts'))
        new_len_posts = len_posts + how_much_to_load
        user_id = request.GET.get('userPk')

        more_posts = list(Post.objects.filter(user_id=user_id).order_by('-created_at')[len_posts:new_len_posts])

        if not more_posts:
            return JsonResponse({'data': False})

        data = [post_data for post_data in UserPostsDynamicLoad.generate_posts_data(more_posts, new_len_posts)]
        return JsonResponse({'data': data})

    @staticmethod
    def generate_posts_data(posts: list, new_len_posts: int):
        for post in posts:
            obj = {
                'id': post.pk,
                'title': post.title,
                'body': post.body,
                'created_at': f'{date(post.created_at)} {time(post.created_at)}',
                'user_pk': post.user_id,
                'len_posts': new_len_posts,
                'url': post.get_absolute_url()
            }

            if post == posts[-1]:
                obj['last_post'] = True

            yield obj


class ShowPost(DetailView):
    """Возвращает ответ(response) с информацией о посте"""
    model = Post
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формируем и возвращаем информацию, которую передаем в шаблон"""
        context = super().get_context_data(**kwargs)  # Получаем context у предка
        context['title'] = context['post']

        # Увеличиваем количество просмотров у поста
        context['views'] = context['post'].post_views
        context['post'].post_views = F('post_views') + 1
        context['post'].save()

        # Самые популярные посты
        context['popular_posts'] = Post.objects.all().order_by('-post_views')[:3]

        return context

    def get_queryset(self):
        return Post.objects.all().select_related('user').prefetch_related('categories')


class LoginUser(LoginView):
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')
