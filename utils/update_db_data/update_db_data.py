# В целом надо все функции менять, тк сейчас используется update_or_create()
# Он нам не подходит, тк он обновляет записи в базе данных без каких либо проверок
# (пока переделал только update_or_create_post)
#
# Также, скорее всего, надо будет все методы изменить на bulk_create() и bulk_update()


import os
import time

import django

from data.config import urls_for_update_db_data as urls


def setup_django():
    """
    Настраивает Django

    При запуске HTTP сервера и выполнении команды Django это происходит автоматически
    """
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "cool_posts_site.settings"
    )
    django.setup()


def update_db_data():
    """
    Обновляет записи в БД

    Доделать:
        добавить проверки на ошибки
    """
    keys = {
        'users': update_or_create_user,
        'posts': update_or_create_post
    }

    while True:
        for key, url in urls.items():
            current_key_function = keys[key]
            data = get_json(url)

            for item in data:
                current_key_function(item)

        time.sleep(60 * 60)  # Останавливает выполнение на 60 минут


if __name__ == '__main__':
    setup_django()
    from utils.update_db_data.update_utils import get_json, update_or_create_user, update_or_create_post

    update_db_data()
