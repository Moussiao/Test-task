from django.db import models
from django.urls import reverse

from misc.models.base_models import TimeBaseModel


class Company(TimeBaseModel):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    catch_phrase = models.CharField(max_length=255, verbose_name='catchPhrase')
    bs = models.CharField(max_length=255, verbose_name='bs')

    class Meta:
        verbose_name = 'Компания пользователя'
        verbose_name_plural = 'Компании пользователей'

    def __str__(self):
        return f'{self.name}'


class UserAddress(TimeBaseModel):
    street = models.CharField(max_length=255, verbose_name='Улица')
    suite = models.CharField(max_length=255, verbose_name='Suite')
    city = models.CharField(max_length=100, verbose_name='Город')
    zipcode = models.CharField(max_length=100, verbose_name='Почтовый индекс')
    geo = models.JSONField(default=dict, verbose_name='Геолокация')

    class Meta:
        verbose_name = 'Адрес пользователя'
        verbose_name_plural = 'Адреса пользователей'

    def __str__(self):
        return f'{self.zipcode} | {self.city} | {self.street}'


class User(TimeBaseModel):
    """
    Модель содержащая информацию о пользователе.

    Атрибут id не является models.AutoField, тк информацию для БД мы берем из другого источника,
    который уже содержит userId.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='Полное имя')
    username = models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя')
    photo = models.ImageField('Фотография', upload_to='users_photo/%Y/%m/%d', null=True)
    email = models.EmailField(verbose_name='Email')
    user_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True,
                                     verbose_name='Адрес пользователя')
    phone_number = models.CharField(max_length=100, verbose_name='Номер телефона')
    user_website = models.CharField(max_length=255, verbose_name='Веб-сайт пользователя')
    user_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True,
                                     verbose_name='Компания пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} | {self.username}'

    def get_absolute_url(self):
        return reverse('get_user', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    """Категории для постов"""
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория для постов'
        verbose_name_plural = 'Категории для постов'


class Post(TimeBaseModel):
    """
    Модель содержащая информацию о посте, который привязан к определенному пользователю.

    Атрибут id не является models.AutoField, тк информацию для БД мы берем из другого источника,
    который уже содержит userId.
    """
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Название поста')
    body = models.TextField(verbose_name='Текст поста')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор поста')
    categories = models.ManyToManyField(PostCategory, default=[])
    post_views = models.PositiveIntegerField('Количество просмотров', default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пользовательские посты'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})
