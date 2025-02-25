
# Note Service: Пример гексагональной архитектуры

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.112.0-green)
![MongoDB](https://img.shields.io/badge/MongoDB-latest-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Note Service** — это демонстрационный микросервис, иллюстрирующий применение гексагональной (портовой) архитектуры на практике. Проект представляет собой сервис управления заметками с REST API, реализованный с использованием лучших практик: разделение бизнес-логики от инфраструктуры, инъекция зависимостей, асинхронность и тестируемость. Он использует FastAPI для API, MongoDB для хранения данных и Prometheus для метрик.

Цель проекта — показать, как гексагональная архитектура помогает создавать гибкие, масштабируемые и поддерживаемые приложения.

---

## Гексагональная архитектура

Гексагональная архитектура (Hexagonal Architecture), также известная как "порты и адаптеры", ставит бизнес-логику в центр приложения, изолируя её от внешних систем (UI, базы данных, API). Это достигается через:

1. **Порты (Domain/Interfaces)**  
   Абстрактные интерфейсы, определяющие, какие операции поддерживает бизнес-логика. Например, `NoteRepository` задаёт контракт для работы с заметками, не привязываясь к конкретной базе данных.

2. **Адаптеры (Infrastructure/Presentation)**  
   Конкретные реализации портов (например, `MongoNoteRepository` для MongoDB) и внешние интерфейсы (REST API в `presentation/api/notes.py`). Адаптеры подключаются к ядру через порты, что позволяет легко заменять технологии.

3. **Ядро (Application/Domain)**  
   Бизнес-логика (`NoteManager`) и доменные модели (`Note`, `User`) не зависят от внешних технологий. Это делает код переносимым и тестируемым.

4. **Инъекция зависимостей (Core)**  
   Через контейнер (`Container`) зависимости передаются в приложение динамически, обеспечивая слабую связанность между слоями.

### Преимущества подхода
- **Гибкость**: Легко заменить MongoDB на другую базу данных, изменив только адаптер.
- **Тестируемость**: Бизнес-логика тестируется с мок-объектами вместо реальных баз данных.
- **Поддерживаемость**: Четкое разделение ответственности упрощает внесение изменений.

**Note Service** служит примером этих принципов в реальном коде.

---

## Структура проекта
```
├── .gitignore                # Игнорируемые файлы (например, .idea/)
├── README.md                 # Документация проекта
├── docker-compose.yml        # Конфигурация Docker Compose
└── note_service              # Основной каталог сервиса
    ├── init.py           # Инициализация пакета и версия
    ├── app                   # Приложение
    │   ├── init.py
    │   ├── application       # Бизнес-логика (ядро)
    │   │   ├── init.py
    │   │   └── note_manager.py
    │   ├── core              # Инструменты и зависимости
    │   │   ├── init.py
    │   │   ├── config.py
    │   │   ├── container.py
    │   │   ├── dependencies.py
    │   │   └── metrics.py
    │   ├── domain            # Домен (порты и модели)
    │   │   ├── init.py
    │   │   ├── interfaces.py
    │   │   └── models
    │   │       ├── init.py
    │   │       ├── note.py
    │   │       └── user.py
    │   ├── infrastructure    # Адаптеры для хранилища
    │   │   ├── init.py
    │   │   └── db.py
    │   ├── main.py           # Точка входа
    │   └── presentation      # Адаптеры для API
    │       ├── init.py
    │       └── api
    │           ├── init.py
    │           └── notes.py
    ├── docker                # Dockerfile
    │   └── Dockerfile
    ├── requirements.txt      # Зависимости проекта
    └── tests                 # Тесты
        ├── .pytest_cache     # Кэш pytest (игнорируется в git)
        │   ├── .gitignore
        │   ├── CACHEDIR.TAG
        │   ├── README.md
        │   └── v
        │       └── cache
        │           ├── lastfailed
        │           ├── nodeids
        │           └── stepwise
        └── test_note_manager.py

```
---

## Возможности сервиса

- **CRUD для заметок**: Создание, чтение, обновление и удаление через REST API.
- **Асинхронность**: Использование `motor` для работы с MongoDB.
- **Метрики**: Сбор данных о запросах через `prometheus-client`.
- **Контейнеризация**: Поддержка Docker и Docker Compose.
- **Тесты**: Проверка бизнес-логики с помощью `pytest` и мок-репозиториев.

Эти функции демонстрируют, как гексагональная архитектура интегрируется с современными инструментами.

---

## Установка и запуск

### Требования
- Docker и Docker Compose
- Python 3.11 (для локального запуска)

### Через Docker Compose
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/RitinaADM/FastAPI_Mongodb_HexaMicro.git
   ```
   ```bash
   cd note-service
    ```

    Запустите сервис:
    ```bash
    docker-compose up --build
    ```
    API доступно на http://localhost:8080.

Локально

Установите зависимости:
    
``` bash 
    cd note_service
```
```bash
    pip install -r requirements.txt
   ```

Запустите MongoDB (по умолчанию: mongodb://localhost:27017).\n
Запустите приложение:
``` bash
    python -m note_service.app.main
```
    API доступно на http://localhost:8000.

API
Swagger-документация: http://localhost:8080/docs.

    POST /api/notes/ — создать заметку.
    GET /api/notes/ — список заметок пользователя.
    GET /api/notes/{note_id} — получить заметку.
    PUT /api/notes/{note_id} — обновить заметку.
    DELETE /api/notes/{note_id} — удалить заметку.

API — это адаптер, подключающий внешний мир к ядру приложения.
Тестирование
Запуск тестов:
bash

cd note_service
pytest tests/

Тесты используют мок-репозитории для проверки NoteManager, демонстрируя независимость бизнес-логики от инфраструктуры. Кэш тестов сохраняется в .pytest_cache (игнорируется в Git). Очистка кэша:
bash

pytest --cache-clear

Метрики
Prometheus собирает:

    note_service_requests_total — количество запросов.
    note_service_request_latency_seconds — задержка запросов.

Игнорируемые файлы
.gitignore исключает:

    .idea/ — настройки PyCharm.
    .pytest_cache/ — кэш pytest.

---
