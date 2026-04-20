
REST API (Wallet API) на FastAPI

Стэк - Python 3.12.4, FastAPI, Pydantic, SQLAlchemy, Alembic, pytest, poetry
-База данных PostgreSQL развернута в докер контейнере (тестовая база так же в контейнере)
-2 основных эндпоинта 
POST  /api/v1/wallets/<WALLET_UUID>/operation 

GET /api/v1/wallets/<WALLET_UUID>
Еще для удобства сделана ручка типа GET /api/v1/wallets/<WALLET_UUID>/all_ids для получения всех id из БД

Для удобства есть функция, которая заполняет БД входными данными, запустить можно так - python -m app.database.make_test_data. Перед этим нужно настроить виртуальное окружение, установить систему контроля зависимостей pip install poetry и сами зависимости poetry install. После нужно поднять докер контейнер командой docker compose up -d 
И применить миграции - alembic upgrade head | alembic -x db=test upgrade head(для тестовой БД)
Документация Swagger http://127.0.0.1:8000/docs для рабоыт с ней запускаем asgi web-server uvicorn командой python -m app.main 

Pytest - интеграционные тесты. Для тестов используются фикстуры клиента, который по http делает запросы внутри FastAPI, фикстура получения сессии для подключения к тестовой БД, а так же dependency_overrides для работы с тестовой базой, есть очистка базы после тестов. Тесты можно запустить командой pytest -v (p.s тесты запускаются корректно только по 1, при сборе и запуске всех сразу появляется ошибка с циклом событий)
