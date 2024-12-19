# Bonus Service REST API

Сервис для просмотра текущего уровня бонусной программы пользователя.

## Запуск

1.  **Клонировать репозиторий:**
    ```bash
    git clone <ссылка_на_ваш_репозиторий>
    cd bonus_service
    ```

2.  **Создать виртуальное окружение и активировать его:**
    ```bash
    python -m venv venv
    source venv/bin/activate # для Linux/macOS
    venv\Scripts\activate # для Windows
    ```

3.  **Установить зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Выполнить миграции базы данных:**
    ```bash
    python manage.py migrate
    ```

5.  **Запустить сервер:**
    ```bash
    python manage.py runserver
    ```

## API Эндпоинты

### Аутентификация сотрудника (получение токена)

-   **URL:** `POST /api/auth/login/`
-   **Метод:** `POST`
-   **Тело запроса (JSON):**
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
-   **Ответ (JSON):**
    ```json
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2OTkxMDU0MjYsInVzZXJuYW1lIjoidGVzdHVzZXIifQ.K2w_v8N_..."
    }
    ```
-   **Описание:** Возвращает JWT токен для последующего доступа к защищенным эндпоинтам.

### Получение данных о бонусах пользователя

-   **URL:** `GET /api/bonuses/`
-   **Метод:** `GET`
-   **Заголовки:**
    ```
    Authorization: Bearer <token>
    ```
-   **Ответ (JSON):**
    ```json
    {
        "current_level": "Серебряный",
        "cashback_percentage": 5,
        "next_level": "Золотой",
        "next_level_threshold": 5000,
         "current_spending": 3000
    }
    ```
-   **Описание:** Возвращает данные о текущем уровне бонусной программы пользователя, его кэшбеке, следующем уровне и пороге для перехода.

## Описание модели данных

### `UserBonuses`
 - `user` (ForeignKey): Ссылка на пользователя (по умолчанию Django User)
 - `current_spending` (Decimal): Сумма текущих трат пользователя
- `level_name` (CharField): Название уровня пользователя (Серебряный, Золотой, Платиновый)
- `cashback_percentage` (IntegerField): Процент кэшбека текущего уровня

### `BonusLevel`
 - `level_name` (CharField): Название уровня (Серебряный, Золотой, Платиновый)
 - `spending_threshold` (Decimal): Порог трат для перехода на данный уровень
 - `cashback_percentage` (IntegerField): Процент кэшбека для этого уровня

## Настройка окружения
1. Создать файл .env в корне проекта
2. Заполнить файл переменными
3. Пример:
SECRET_KEY="secret_key_for_django"
DEBUG=True
ALLOWED_HOSTS="127.0.0.1"
TOKEN_EXPIRATION_TIME=36000
## Зависимости

-   Django
-   Django REST Framework
-   PyJWT
-   python-decouple

## Примечания

-   При запуске по умолчанию создается 1 суперпользователь с логином admin и паролем admin.
-   Токены валидны в течение 1 часа по умолчанию.