# API-Tests

Учебный проект API-автотестов для REST-сервиса управления сущностями.

**Стек:** Python · pytest · requests · pydantic · allure-pytest · pytest-xdist

---

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Запустить бэкенд
docker compose up -d

# 3. Запустить все тесты
pytest -v

# 4. Открыть Allure-отчёт
allure serve allure-results
```

---

## Тест-кейсы

| ID    | Эндпоинт                           | Что проверяется                              |
|-------|------------------------------------|----------------------------------------------|
| TC-01 | `POST /api/create`                 | Создание сущности, ответ содержит числовой ID |
| TC-02 | `GET /api/get/{id}`                | Получение сущности, объект десериализован    |
| TC-03 | `GET /api/getAll`                  | Список сущностей, ответ является массивом    |
| TC-04 | `PATCH /api/patch/{id}`            | Обновление сущности, статус 204              |
| TC-05 | `DELETE /api/delete/{id}`          | Удаление сущности, статус 204                |
| TC-06 | `GET /api/getAll?title=...`        | Фильтрация по title работает корректно       |
| TC-07 | `GET /api/getAll?verified=true`    | Фильтрация по verified работает корректно    |
| TC-08 | `GET /api/getAll?page=1&perPage=1` | perPage ограничивает количество результатов  |

Подробное описание каждого кейса - в [TEST_CASES.md](TEST_CASES.md).

---

## Структура проекта

```
API-Tests/
├── conftest.py               фикстуры pytest: base_url, created_entity_id
├── config.py                 константы (BASE_URL)
├── pytest.ini                настройки pytest и Allure
├── requirements.txt
├── docker-compose.yml        запуск бэкенда для CI
├── .gitignore
├── .github/
│   └── workflows/
│       └── tests.yml         CI/CD: запуск тестов, сохранение Allure-артефакта
├── api/
│   └── entity_api.py         POM-класс: все HTTP-вызовы к API
├── builders/
│   └── entity_builder.py     Fluent Builder для формирования тела запроса
├── models/
│   ├── requests.py           Pydantic-модели запросов
│   └── responses.py          Pydantic-модели ответов
└── tests/
    └── test_entity.py        8 тест-кейсов
```

---

## Архитектура

Паттерн **POM (Page Object Model)**, адаптированный для API: один класс `EntityApi` на один ресурс.  
Класс инкапсулирует все HTTP-вызовы - тесты не знают про `requests` и URL.

```
tests/test_entity.py  ->  api/entity_api.py  ->  requests  ->  сервер
```

Тела запросов собираются через **Fluent Builder**:

```python
entity = (EntityRequestBuilder()
    .title("Тест")
    .verified(True)
    .important_numbers([1, 2, 3])
    .addition("Инфо", 42)
    .build())
```


## Полезные команды

```bash
# Один конкретный тест
pytest -v tests/test_entity.py::test_create_entity

# Параллельный запуск
pytest -v -n 2

# Повторить только упавшие тесты
pytest -v --lf
```

---

## Ограничения

- Бэкенд-сервис должен быть запущен на `http://localhost:8080` до начала тестов
- Параллельный запуск (`-n`) может быть нестабилен — локальный Docker имеет ограниченный пул соединений к БД
