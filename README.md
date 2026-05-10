# Cian Studios API

## Описание проекта

Проект выполнен в рамках блока «Продвинутая web-разработка на Python».

Цель проекта — создать API-интерфейс для взаимодействия с данными, собранными в прошлом проекте со скрапера ЦИАН.

API позволяет получать небольшой срез данных из SQLite-базы объявлений об аренде студий в ЮВАО Москвы.

Источник данных: база `data/cian_studios.db`, полученная в предыдущем проекте.

## Что реализовано

- FastAPI-приложение
- автоматическая документация Swagger UI
- получение списка объявлений
- фильтрация по цене и площади
- сортировка
- ограничение размера ответа
- получение объявления по id
- получение общей статистики

## Структура проекта

```text
cian_api_project/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── queries.py
│   └── schemas.py
├── data/
│   └── cian_studios.db
├── artifacts/
│   └── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск API

```bash
uvicorn app.main:app --reload
```

После запуска API будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Документация Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Эндпоинты

### Проверка работы API

```http
GET /health
```

### Получение списка объявлений

```http
GET /listings
```

Параметры:

- `limit` — количество записей, от 1 до 100
- `offset` — смещение
- `min_price` — минимальная цена
- `max_price` — максимальная цена
- `min_area` — минимальная площадь
- `max_area` — максимальная площадь
- `sort_by` — поле сортировки: `price_rub`, `area_m2`, `scraped_at`, `listing_id`
- `sort_order` — порядок сортировки: `asc` или `desc`

Пример:

```text
http://127.0.0.1:8000/listings?min_price=40000&max_price=70000&limit=10&sort_by=price_rub&sort_order=asc
```

### Получение объявления по id

```http
GET /listings/{listing_id}
```

### Статистика

```http
GET /stats
```

## Ограничения

API не отдаёт всю базу целиком. Максимальное значение `limit` для `/listings` — 100 записей.

Реализована базовая валидация параметров:

- `limit` не может быть больше 100
- `offset` не может быть отрицательным
- `min_price` не может быть больше `max_price`
- `min_area` не может быть больше `max_area`
- сортировать можно только по разрешённым полям

## Артефакты запуска

Для сдачи можно приложить скриншоты:

- страницы `http://127.0.0.1:8000/docs`
- ответа эндпоинта `/listings`
- ответа эндпоинта `/stats`

Скриншоты можно сохранить в папку:

```text
artifacts/screenshots/
```
