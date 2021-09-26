from collections import OrderedDict
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag()
def url_replace(request, field, value, direction=''):
    """
    Возвращает URL с новым заданным параметром HTTP GET, сохраняя существующие параметры.

    Если словарный объект, содержащий все заданные параметры HTTP GET, уже содержит параметр с ключом 'order_by',
    то мы либо добавляем к параметру знак '-', либо убираем данный знак.
    Использование '-' указывает на то, что необходимо сортировать по убыванию. Без '-' по вовзрастанию.
    """
    query_dict = request.GET.copy()  # Словарь содержащий уже заданные параметры HTTP GET

    if field == 'order_by' and field in query_dict.keys():
        if query_dict[field].startswith('-') and query_dict[field].lstrip('-') == str(value):
            query_dict[field] = str(value)
        elif query_dict[field].lstrip('-') == str(value):
            query_dict[field] = '-' + str(value)
        else:
            query_dict[field] = direction + str(value)

    elif field == 'search' and field in query_dict.keys():
        if value:
            query_dict[field] = str(value)
        else:
            del query_dict[field]

    else:
        query_dict[field] = direction + str(value)

    return urlencode(OrderedDict(sorted(query_dict.items())))
