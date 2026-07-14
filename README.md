# Трекер привычек

## Описание
Веб-приложение для отслеживания привычек с уведомлениями в Telegram.

## Технологии
- Django 5.1
- PostgreSQL
- Redis
- Celery
- Nginx
- Docker

## Локальный запуск

### Требования
- Docker и Docker Compose
- Git

### Установка и запуск
1. Клонируйте репозиторий:
git clone https://github.com/yourusername/tracker.git
cd tracker

2. Настройте переменные окружения:
cp .env.example .env
3. Запустите проект:
docker compose up -d
4. Примените миграции:
docker compose exec backend python manage.py migrate
5. Создайте суперпользователя:
docker compose exec backend python manage.py createsuperuser

Доступ к приложению
API: http://localhost:8000

Админка: http://localhost:8000/admin

Swagger: http://localhost:8000/swagger/

CI/CD
При пуше в ветку main автоматически:

Запускаются тесты и линтинг

Собираются Docker-образы

Выполняется деплой на сервер

Структура сервисов
backend — Django приложение

db — PostgreSQL

redis — Redis

celery — Celery worker

celery-beat — Celery beat

nginx — Веб-сервер

Автор
Wizard