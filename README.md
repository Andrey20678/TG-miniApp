# Руководство по установке
Перед использованием создать файлы в папке config

bot.env
```.env
BOT_TOKEN   = "Token"
SECRET_KEY  = "Secret key"

#Optional 
ADMIN_ID    = "telegram_user_id"
```
webflow.env
```.env
API_KEY       = "Token"
COLLECTION_ID = "ID"
SITE_ID       = "ID"
```

Создать и\или активировать виртуальное окружение

(Windows)
```
py -m venv .venv
.\.venv\Scripts\activate
```
(Linux)
```
python3 -m venv .venv
source .venv/bin/activate
```
Установить зависимости
```commandline
pip install fastapi[standard] aiogram pydantic-settings
```
### Запустить main.py

Для работы необходим хостинг веб сервера (Nginx, VS Code или др.)