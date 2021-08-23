# Описание сервиса:
### *Как Кинопоиск, только хуже :)*
### API для сервиса, который собирает отзывы на произведения искусства:
- Кино
- Музыка
- Книги


## Возможности:
- Создание аккаунта пользователя
- Публикация, изменение, удаления отзывов к произведениям
- Публикация, изменение, удаления коментариев к отзывам
- Реализованы поиск и фильтрация в запросах


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/pakodev28/api_yamdb.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```


## Команды для загрузки данных из csv в базу данных:

загрузить категории
```
python3 manage.py load_category_data
```
загрузить жанры
```
python3 manage.py load_genre_data
```
загрузить тайтлы
```
python3 manage.py load_title_data
```
```
python3 manage.py load_genre_title_data
```
загрузить отзывы
```
python3 manage.py load_review_data
```
загрузить коментарии
```
python3 manage.py load_comments_data
```
загрузить пользователей
```
python3 manage.py load_users_data
```

## Подробную документацию с примерами запросов вы найдете по адресу:
http://127.0.0.1:8000/redoc/
