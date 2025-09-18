# FastAPI test project

## Тестовый проект на FastApi

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

!!! Не забудьте добавить файл .env в .gitignore.
Информация, как получить API ключи для Deepseek и Unsplash ниже.

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
