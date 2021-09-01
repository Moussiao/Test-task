from json.decoder import JSONDecodeError
from typing import List

import requests
from django.db.models import Model

from strange_posts.models import User, Company, Post, UserAddress


def print_update(obj, created: bool):
    print(f'Обновление {obj}\n'
          f'Создан: {created}')


def get_json(url) -> List[dict]:
    """
    Возвращает dict с данными из json ответа

    Доделать:
        вместо return [] вызывать exceptions
    """
    response = requests.get(url=url)

    if response.status_code is not requests.codes.ok:
        return []

    try:
        json_response = response.json()
    except JSONDecodeError:
        return []
    else:
        if not json_response:
            return []

    return json_response


def db_model_contains_kwargs(db_model: Model, **kwargs) -> bool:
    """
    Проверяет есть ли в экземпляре класса атрибуты с именами из kwargs.
    Если атрибуты есть и их значения равны значениям из kwargs, то возвращает True
    Если хоть одно значение атрибута не равно значению из kwargs, то False
    """
    for key, value in kwargs.items():
        db_attr = getattr(db_model, key)
        if db_attr != value:
            return False

    return True


def update_or_create_address(address_data: dict, *, update: bool = False, address_id: int = 0):
    if update:
        address, created = UserAddress.objects.update_or_create(pk=address_id, defaults={**address_data})
    else:
        address, created = UserAddress.objects.get_or_create(**address_data)
        address.save()

    print_update(address, created)
    return address


def update_or_create_company(company_data: dict, *, update: bool = False, company_id: int = 0):
    company_data = {
        'name': company_data['name'],
        'catch_phrase': company_data['catchPhrase'],
        'bs': company_data['bs']
    }

    if update:
        company, created = Company.objects.update_or_create(pk=company_id, defaults={**company_data})
    else:
        company, created = Company.objects.get_or_create(**company_data)

    print_update(company, created)
    return company


def update_or_create_post(post_data: dict):
    """
    Обновляет или создает Post в БД

    Если Post уже создан и его значения не равны загруженным значениям,
    то его значения обновляются на новые.
    """
    defaults = {
        'title': post_data['title'],
        'body': post_data['body']
    }

    post, created = Post.objects.get_or_create(id=post_data['id'], user_id=post_data['userId'], defaults=defaults)

    if not created and not db_model_contains_kwargs(post, **defaults):
        post.title = defaults['title']
        post.body = defaults['body']
        post.save()

    print_update(post, created)
    return post


def update_or_create_user(user_data: dict):
    defaults = {
        'name': user_data['name'],
        'username': user_data['username'],
        'email': user_data['email'],
        'phone_number': user_data['phone'],
        'user_website': user_data['website']
    }

    user, created = User.objects.update_or_create(id=user_data['id'], defaults=defaults)

    if created:
        user.user_address = update_or_create_address(address_data=user_data['address'])
        user.user_company = update_or_create_company(company_data=user_data['company'])
    else:
        user.user_address = update_or_create_address(address_data=user_data['address'], update=True,
                                                     address_id=user.user_address_id)
        user.user_company = update_or_create_company(company_data=user_data['company'], update=True,
                                                     company_id=user.user_company_id)

    user.save()

    print_update(user, created)
    return user


# def update_or_create_address2(address_data: dict, address_id: int = 0) -> Tuple[Model, bool]:
#     address, created = UserAddress.objects.get_or_create(defaults={**address_data})
#
#     if not created and not db_model_contains_kwargs(address, **address):
#         address.street = address_data['street']
#         address.suite = address_data['suite']
#         address.city = address_data['city']
#         address.zipcode = address_data['zipcode']
#         address.geo = address_data['geo']
#
#         address.save()
#         return address, True
#
#     return address, False
#
#
# def update_or_create_company2(company_data: dict, company_id: int = 0) -> Tuple[Model, bool]:
#     defaults = {
#         'name': company_data['name'],
#         'catch_phrase': company_data['catchPhrase'],
#         'bs': company_data['bs']
#     }
#
#     company, created = Company.objects.get_or_create(**company_data)
#
#     if not created and not db_model_contains_kwargs(company, **company_data):
#         company.name = defaults['name']
#         company.catch_phrase = defaults['catchPhrase']
#         company.bs = defaults['bs']
#
#         company.save()
#         return company, True
#
#     return company, False
