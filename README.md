# Тестовое задание
[![wakatime](https://wakatime.com/badge/github/Moussiao/Test-task.svg)](https://wakatime.com/badge/github/Moussiao/Test-task)
<br />
Если python < python 3.9, то https://django.fun/docs/django/ru/3.2/ref/databases/#enabling-json1-extension-on-sqlite <br /><br />
Загрузка в локальную БД данных пользователей и постов: utils/update_db_data/update_db_data.py

### Реализовал: 
Возможность сортировки таблицы по определенным значениям, динамическую загрузку постов, постраничную навигацию

### Дополнение:
Только в конце понял, что необходимо переделать update_db_data.py, тк слишком много времени уходит при использовании update_or_create()
<br /><br />
Переделал только функцию update_or_create_post
<br /><br />
И похоже я с самого начала неверно это реализовал, так как, скорее всего, лучше использовать bulk_create() и bulk_update()