# Описание API
Это API предоставляет функционал для сокращения ссылок с аутентификацией пользователей и управлением ссылками.
![photo_2025-04-01_23-28-18](https://github.com/user-attachments/assets/c4f19734-7b45-42bb-a1b7-27f421a4f388)

## Аутентификация

API использует OAuth2 с потоком паролей:
1. Регистрация пользователя через /register
2. Вход и получение токена через /token
3. Использование токена в последующих запросах (Authorization: Bearer <токен>)

## Конечные точки (Endpoints)

### Управление ссылками

- POST /links/shorten - Создать новую короткую ссылку
  - Требуется аутентификация
  - Тело запроса: схема CreateLink (URL, опционально пользовательский алиас и срок действия)
  
- GET /links/{short_code} - Перенаправление на оригинальный URL
  - Без аутентификации
  
- PUT /links/{short_code} - Обновить короткую ссылку
  - Требуется аутентификация
  - Тело запроса: схема UpdateLink
  
- DELETE /links/{short_code} - Удалить короткую ссылку
  - Требуется аутентификация

### Информация о ссылках

- GET /links/{short_code}/stats - Получить статистику по короткой ссылке
  - Без аутентификации

- GET /links/search?original_url={url} - Поиск существующих коротких кодов по оригинальному URL
  - Без аутентификации

### Управление пользователями

- POST /register - Зарегистрировать нового пользователя
  - Тело запроса: схема ModelUser (логин и пароль)
  
- POST /login - Вход пользователя
  - Тело запроса: схема ModelUser
  
- POST /token - Получить OAuth2 токен
  - Форма данных: username, password, grant_type=password

### Прочие

- GET /secured - Пример защищенного endpoint
  - Требуется аутентификация
  
- GET / - Корневой endpoint
  - Без аутентификации

## Схемы данных

### CreateLink
- url (обязательно): Оригинальный URL для сокращения
- custom_alias: Опциональный пользовательский короткий код
- expires_at: Опциональная дата истечения срока действия

### UpdateLink
- short_code: Короткий код для обновления
- url: Новый целевой URL
- expires_at: Новая дата истечения срока действия

### ModelUser
- login (обязательно)
- password (обязательно)

### Token
- access_token: Токен для аутентификации
- token_type: Всегда "bearer"

# Примеры запросов
![photo_2025-04-01_23-31-35](https://github.com/user-attachments/assets/163b6326-9ab2-4036-b889-d277dc08ca01)
curl -X 'POST' \
  'http://0.0.0.0:8007/links/shorten' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "string",
  "custom_alias": "strшing",
  "expires_at": "2025-04-01T20:30:56.385Z"
}'

![photo_2025-04-01_23-32-05](https://github.com/user-attachments/assets/e768e3a1-9319-4495-810f-c176a0c0ef14)
curl -X 'GET' \
  'http://0.0.0.0:8007/links/str%D1%88ing' \
  -H 'accept: application/json'

![photo_2025-04-01_23-37-09](https://github.com/user-attachments/assets/5245604a-6e22-4bd0-bf91-574b483a89ad)
curl -X 'PUT' \
  'http://0.0.0.0:8007/links/str%D1%88ing' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6IjEyMyIsImVudiI6bnVsbCwidXNlciI6MiwiZXhwIjoxNzQzNjM3MDAyfQ.bV0KNNB16yaG-geVJksnvAQN1raVQ1NW-n_2qIOHqj8' \
  -H 'Content-Type: application/json' \
  -d '{
  "short_code": "strsng",
  "url": "string",
  "expires_at": "2025-04-01T20:33:04.913Z"
}'

![photo_2025-04-01_23-37-47](https://github.com/user-attachments/assets/76ced835-84c8-4828-a132-a0b5a6b7bf84)
curl -X 'DELETE' \
  'http://0.0.0.0:8007/links/strinwg' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6IjEyMyIsImVudiI6bnVsbCwidXNlciI6MiwiZXhwIjoxNzQzNjM3MDAyfQ.bV0KNNB16yaG-geVJksnvAQN1raVQ1NW-n_2qIOHqj8'

# Инструкция по запуску


# Описание БД
![photo_2025-04-01_23-34-24](https://github.com/user-attachments/assets/fba9f7a7-bf94-4637-a3a7-5baf697333d5)
