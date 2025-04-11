# Тестовое задание для компании Mycego

# Web-приложение для работы с API Яндекс.Диска 

Это веб-приложение на Django, которое взаимодействует с API Яндекс.Диска. Оно позволяет пользователю:
1. Просматривать файлы и папки по публичной ссылке.
2. Загружать выбранные файлы на локальный компьютер.

## Требования

- Python 3.6+
- Django 3.x+
  

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/GSlav080/Test_task_mycego.git
    cd your-repo
    ```

2. Создайте виртуальное окружение (Для Windows):

    ```bash
    python -m venv venv
    venv\Scripts\activate 
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```


## Запуск

1. Выполните миграции:

    ```bash
    python manage.py migrate
    ```

2. Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

3. Откройте браузер и перейдите по адресу:

    ```
    http://127.0.0.1:8000
    ```

4. Введите публичную ссылку на Яндекс.Диск, чтобы увидеть список файлов.

## Функционал

- Просмотр файлов с Яндекс.Диска.
- Загрузка файлов на локальный компьютер.

## Дополнительные функции 

- Фильтрация файлов по типу.
- Возможность скачивания нескольких файлов одновременно (zip архив с уникальным названием).
- Кэширование списка файлов(3 минуты).




