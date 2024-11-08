# YaCut

**YaCut** — это веб-сервис для укорачивания ссылок, который связывает длинные URL с короткими. Пользователи могут
задавать собственные короткие идентификаторы или использовать автоматически сгенерированные ссылки.

## Оглавление

- [Описание проекта](#описание-проекта)
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [Использование](#использование)
- [API](#api)

## Описание проекта

На многих сайтах URL-адреса страниц могут быть слишком длинными и неудобными для использования. YaCut позволяет
сократить такие ссылки, чтобы было проще делиться ими. Сервис поддерживает как пользовательские короткие ссылки, так и
автоматически сгенерируемые.

Ключевые возможности:

- **Генерация коротких ссылок**: ассоциация длинного URL с уникальным коротким идентификатором.
- **Редирект**: переход на исходный адрес при обращении по короткой ссылке.
- **API**: взаимодействие через RESTful API для создания и получения ссылок.

### Основные функции

1. Пользователь вводит длинную ссылку и получает короткий URL.
2. Пользователь может задать свой вариант короткого идентификатора (не более 16 символов).
3. Если пользовательский идентификатор занят, то выдается уведомление.
4. Если идентификатор не указан, сервис генерирует его автоматически (6 случайных символов: буквы и цифры).

## Технологии

Проект разработан на **Flask** и использует **SQLAlchemy** (по умолчанию используется SQLite).

## Установка и запуск

1. Клонируйте репозиторий с GitHub:
   ```bash
   git clone
   cd yacut
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` с переменными окружения, например:
   ```env
    FLASK_APP=yacut
    FLASK_ENV=development
    DATABASE_URI=sqlite:///db.sqlite3
    SECRET_KEY=1243
    ENDPOINT=http://localhost/
   ```

5. Запустите сервер:
   ```bash
   flask run
   ```

## Использование

Откройте браузер и перейдите на `http://127.0.0.1:5000/`. На главной странице сервиса находится форма с двумя полями:

- Поле для длинного URL (обязательно).
- Поле для короткого идентификатора (необязательно).

После отправки формы вы получите короткую ссылку, которая перенаправит на исходный URL.

## API

### Эндпоинты

1. **POST /api/id/** — создание новой короткой ссылки.
    - Тело запроса должно содержать JSON с полями:
        - `original`: исходный URL.
        - `custom_id` (опционально): пользовательский короткий идентификатор.
    - Пример запроса:
      ```json
      {
        "original": "https://example.com/long-url",
        "custom_id": "example"
      }
      ```

2. **GET /api/id/<short_id>/** — получение исходного URL по короткому идентификатору.
    - Пример запроса: `GET /api/id/example/`
    - Ответ:
      ```json
      {
        "original": "https://example.com/long-url"
      }
      ```

### Обработка ошибок

- 400: Неверный запрос (например, короткий идентификатор уже занят).
- 404: Ссылка не найдена (неверный `short_id`).
