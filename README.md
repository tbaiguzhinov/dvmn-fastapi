# AI генератор сайтов

Данный проект является проектом ИИ генератора сайтов. После получения текстового описания задачи от пользователя, код отправляет запрос в ИИ DeepSeek, где происходит генерация html-кода вебсайта на заданную тему. С помощью Unsplash подбираются картинки, соответствующие теме. После завершение генерации, готовый код сохраняется локально, с помощью Gotenberg создается скриншот, и все сохраняется в S3 хранилище MinIO.


## Порядок действий для запуска кода

### Локальный запуск

1. Скачать данный код с помощью команды:

```bash
git clone git@github.com:tbaiguzhinov/dvmn-fastapi.git
```

2. Перейти в папку:
```bash
cd dvmn-fastapi
```

3. Создать виртуальное окружение и установить зависимости компаний:

```bash
uv sync
```

4. Активировать виртуальное окружение:

```bash
source .venv/bin/activate
```

5. Создать в корневой папке файл .env с переменными окружения. Примеры переменных присутствуют в файле example.env.

```bash
cp example.env .env
```

Информация, как получить API ключи для Deepseek и Unsplash ниже.  
Подробная информация о переменных окружения приведена ниже.  

6. Запустить работу приложения командой:

```bash
fastapi dev src/main.py
```

7. Сервер будет доступен по умолчанию на http://127.0.0.1:8000. Документация будет по адресу http://127.0.0.1:8000/docs.


Инструкции и справочная информация по разворачиванию локальной инсталляции собраны
в документе [CONTRIBUTING.md](./CONTRIBUTING.md).


### Ссылки для получения API ключей

- [Deepseek](https://api-docs.deepseek.com/)  
- [Unsplash](https://unsplash.com/documentation#creating-a-developer-account)

### Переменные окружения

Для корректной работы кода, а также для более тонкой настройки используются следующие переменные окружения: 

- DEBUG - работа в режиме дебага (True/False)
- DEEPSEEK__API_KEY - API ключ от ИИ DeepSeek
- DEEPSEEK__MAX_CONNECTIONS - (Опционально) Число максимальных соединений для ИИ DeepSeek
- UNSPLASH__API_KEY - API ключ Unsplash
- UNSPLASH__MAX_CONNECTIONS - (Опционально) Число максимальных соединений для Unsplash
- UNSPLASH__TIMEOUT - (Опционально) Время таймаута подключения Unsplash
- MINIO__API_ENDPOINT - Эндпойнт для API MinIO (http://localhost:9000 по умолчанию при работе локально)
- MINIO__LOGIN - Логин для MinIO (minioadmin по умолчанию)
- MINIO__PASSWORD - Пароль для MinIO (minioadmin по умолчанию)
- MINIO__BUCKET - Имя бакета MinIO
- MINIO__CONNECTION_TIMEOUT - (Опционально) Таймаут подключения (10 по умолчанию)
- MINIO__READ_TIMEOUT - (Опционально) Таймаут чтения (30 по умолчанию)
- MINIO__MAX_POOL_CONNECTIONS - (Опционально) Число максимальных соединений (50 по умолчанию)
- GOTENBERG__BASE_URL - Базовый урл для Gotenberg
- GOTENBERG__WIDTH - Ширина скришнота в пикселях для Gotenberg
- GOTENBERG__FORMAT - Формат скришнота (jpeg, png или webp, JPEG по умолчанию) для Gotenberg
- GOTENBERG__WAIT_DELAY - Время ожидания для завершения анимации для Gotenberg
- GOTENBERG__TIMEOUT - Время таймаута чтения для Gotenberg
- GOTENBERG__MAX_CONNECTIONS - Число максимальных соединений для Gotenberg
