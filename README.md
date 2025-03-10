
# HexaMicro Service: Пример микросервисов с гексагональной архитектуры

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.112.0-green)
![MongoDB](https://img.shields.io/badge/MongoDB-latest-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
Python
FastAPI
MongoDB
RabbitMQ
License
Note Service и User Service — это демонстрационный проект, иллюстрирующий применение микросервисной архитектуры в сочетании с гексагональным (портовым) подходом. Проект состоит из двух независимых сервисов:

    Note Service: Управление заметками пользователей через REST API.
    User Service: Управление пользователями, включая регистрацию, аутентификацию и авторизацию.

Цель проекта — показать, как микросервисы взаимодействуют между собой, используя современные технологии (FastAPI, MongoDB, RabbitMQ) и принципы гексагональной архитектуры для обеспечения гибкости, масштабируемости и тестируемости.
Микросервисная архитектура
Проект разделён на два автономных микросервиса, каждый из которых выполняет свою задачу:

    User Service:
        Отвечает за регистрацию, аутентификацию и управление пользователями.
        Генерирует JWT-токены для авторизации.
        Интегрируется с RabbitMQ для асинхронной обработки событий (например, создание пользователей).
    Note Service:
        Управляет заметками, привязанными к пользователям.
        Проверяет JWT-токены, выданные User Service, для авторизации запросов.

Микросервисы взаимодействуют через:

    REST API: Note Service запрашивает данные о пользователях через токены, выданные User Service.
    Сообщения: Возможна асинхронная интеграция через RabbitMQ (например, уведомления о создании пользователей).

Каждый сервис использует собственную базу данных MongoDB, что обеспечивает независимость и изолированность данных.
Гексагональная архитектура
Гексагональная архитектура применяется в обоих сервисах для изоляции бизнес-логики от внешних систем. Основные принципы:

    Порты (Domain/Interfaces)
    Абстрактные интерфейсы задают контракты для операций:
        В Note Service: NoteRepository определяет операции с заметками.
        В User Service: UserRepository определяет операции с пользователями.
    Адаптеры (Infrastructure/Presentation)  
        Infrastructure: MongoNoteRepository и MongoUserRepository реализуют работу с MongoDB, а RabbitMQBroker — с RabbitMQ.
        Presentation: REST API в notes.py (Note Service) и auth.py/users.py (User Service) выступают внешними адаптерами.
    Ядро (Application/Domain)  
        Бизнес-логика (NoteManager и UserManager) и доменные модели (Note, User) изолированы от инфраструктуры.
        Это позволяет тестировать логику независимо от базы данных или внешних сервисов.
    Инъекция зависимостей (Core)  
        Container в каждом сервисе управляет зависимостями, динамически подключая адаптеры к ядру.

Преимущества подхода

    Модульность: Легко заменить MongoDB на PostgreSQL или RabbitMQ на Kafka, обновив только адаптеры.
    Тестируемость: Бизнес-логика проверяется с мок-объектами.
    Масштабируемость: Микросервисы можно разворачивать и масштабировать независимо.
    Поддерживаемость: Четкое разделение слоев и сервисов упрощает разработку и отладку.

Структура проекта
```
├── .gitignore                # Игнорируемые файлы
├── README.md                 # Документация
├── docker-compose.yml        # Конфигурация Docker Compose
├── img.png                   # Изображение (опционально)
├── note_service              # Сервис заметок
│   ├── .env                  # Переменные окружения
│   ├── __init__.py           # Инициализация пакета и версия
│   ├── app                   # Приложение
│   │   ├── __init__.py
│   │   ├── application       # Бизнес-логика
│   │   │   ├── __init__.py
│   │   │   └── note_manager.py
│   │   ├── core              # Инструменты и зависимости
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── container.py
│   │   │   ├── dependencies.py
│   │   │   └── metrics.py
│   │   ├── domain            # Домен (порты и модели)
│   │   │   ├── __init__.py
│   │   │   ├── interfaces.py
│   │   │   └── models
│   │   │       ├── __init__.py
│   │   │       ├── note.py
│   │   │       └── user.py
│   │   ├── infrastructure    # Адаптеры для базы данных
│   │   │   ├── __init__.py
│   │   │   └── db.py
│   │   ├── main.py           # Точка входа
│   │   └── presentation      # Адаптеры для API
│   │       ├── __init__.py
│   │       └── api
│   │           ├── __init__.py
│   │           └── notes.py
│   ├── docker                # Конфигурация Docker
│   │   └── Dockerfile
│   └── requirements.txt      # Зависимости
└── user_service              # Сервис пользователей
    ├── .env                  # Переменные окружения
    ├── __init__.py           # Инициализация пакета и версия
    ├── app                   # Приложение
    │   ├── __init__.py
    │   ├── application       # Бизнес-логика
    │   │   ├── __init__.py
    │   │   └── user_manager.py
    │   ├── core              # Инструменты и зависимости
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── config.py
    │   │   ├── container.py
    │   │   ├── dependencies.py
    │   │   └── metrics.py
    │   ├── domain            # Домен (порты и модели)
    │   │   ├── __init__.py
    │   │   ├── interfaces.py
    │   │   └── models
    │   │       ├── __init__.py
    │   │       └── user.py
    │   ├── infrastructure    # Адаптеры для базы данных и брокера
    │   │   ├── __init__.py
    │   │   ├── db.py
    │   │   └── rabbitmq.py
    │   ├── main.py           # Точка входа
    │   └── presentation      # Адаптеры для API
    │       ├── __init__.py
    │       └── api
    │           ├── __init__.py
    │           ├── auth.py
    │           └── users.py
    ├── docker                # Конфигурация Docker
    │   └── Dockerfile
    └── requirements.txt      # Зависимости
```

Возможности проекта
Note Service

    CRUD для заметок: Создание, чтение, обновление и удаление заметок через REST API.
    Аутентификация: Проверка JWT-токенов для доступа к заметкам только владельца.
    Асинхронность: Использование motor для работы с MongoDB.

User Service

    Управление пользователями: Регистрация, аутентификация, обновление и удаление пользователей.
    Роли: Поддержка ролей user и admin с ограничением доступа.
    Аутентификация: Генерация JWT-токенов и хеширование паролей с bcrypt.
    События: Асинхронная обработка через RabbitMQ.

Общие возможности

    Метрики: Сбор данных о запросах через prometheus-client.
    Контейнеризация: Docker и Docker Compose для развертывания.
    Логирование: Подробные логи с использованием стандартного формата Python.

Установка и запуск
Требования

    Docker и Docker Compose
    Python 3.11 (для локального запуска)

Через Docker Compose

    Склонируйте репозиторий:
    bash

    git clone <repository-url>
    cd <repository-name>

    Запустите сервисы:
    bash

    docker-compose up --build

        User Service: API доступно на http://localhost:8001.
        Note Service: API доступно на http://localhost:8002.
        RabbitMQ: Управление на http://localhost:15672 (guest/guest).

Локально

    Установите зависимости для каждого сервиса:
    bash

    cd note_service
    pip install -r requirements.txt
    cd ../user_service
    pip install -r requirements.txt

    Запустите MongoDB и RabbitMQ (по умолчанию: mongodb://localhost:27017, amqp://guest:guest@localhost:5672/).
    Запустите сервисы:
        Note Service:
        bash

        cd note_service
        python -m note_service.app.main

        User Service:
        bash

        cd user_service
        python -m user_service.app.main

API
User Service
Swagger-документация: http://localhost:8001/docs.

    POST /api/auth/register — Регистрация пользователя (всегда роль user).
    POST /api/auth/login — Получение JWT-токена.
    GET /api/users/ — Список всех пользователей (только для admin).
    GET /api/users/me — Информация о текущем пользователе.
    POST /api/users/me/password — Смена пароля.
    GET /api/users/{user_id} — Получение пользователя (себя или для admin).
    PUT /api/users/{user_id} — Обновление пользователя (себя или для admin).
    DELETE /api/users/{user_id} — Удаление пользователя (себя или для admin).
    POST /api/users/{user_id}/reset-password — Сброс пароля (только для admin).

Note Service
Swagger-документация: http://localhost:8002/docs.

    POST /api/notes/ — Создать заметку.
    GET /api/notes/ — Список заметок текущего пользователя.
    GET /api/notes/{note_id} — Получить заметку.
    PUT /api/notes/{note_id} — Обновить заметку.
    DELETE /api/notes/{note_id} — Удалить заметку.

API в обоих сервисах — это адаптеры, связывающие внешний мир с ядром приложения.
Тестирование
Тесты можно запустить для каждого сервиса:
bash

cd note_service
pytest
cd ../user_service
pytest

    Тесты используют мок-репозитории для проверки NoteManager и UserManager.
    Кэш тестов сохраняется в .pytest_cache (игнорируется в .gitignore).

Очистка кэша:
bash

pytest --cache-clear

Метрики
Prometheus собирает метрики:

    {service}_requests_total — Общее количество запросов (по методам и эндпоинтам).
    {service}_request_latency_seconds — Задержка запросов.

Где {service} — note_service или user_service.
Игнорируемые файлы
.gitignore исключает:

    .idea/ — настройки PyCharm.
    .pytest_cache/ — кэш pytest.
    note_service/.env, user_service/.env — файлы окружения.

Этот проект демонстрирует, как микросервисная архитектура в сочетании с гексагональным подходом позволяет создавать современные, гибкие и масштабируемые приложения.