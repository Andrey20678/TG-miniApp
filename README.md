# Руководство по установке
Перед использованием создать папку config,

файлы bot.env
```.env
BOT_TOKEN   = "Токен"
WEB_HOOK    = "example.org"
BUTTON_URL  = "example.org"

#Optional 
ADMIN_ID    = <user_id>

MEETING_TEXT= Добро пожаловать!
BUTTON_TEXT = Главная страница
HELP_TEXT   = Просто введи /start и нажми на кнопку
```
и webflow.env (можно оставить как написано ниже, в даный момент не используется)
```.env
API_KEY       = "Ключ"
COLLECTION_ID = "id коллекции cms"
```

Создать и\или активировать виртуальное окружение
```commandline
py -m venv .venv
./.venv/Scripts/activate
```
Установить зависимости
```commandline
pip install fastapi[standard] aiogram pydantic-settings
```
### Запустить main.py
(можно из проводника или находясь в корневой папке проекта)

Порт по умолчанию 3001, можно изменить в конце main.py

Для работы необходим хостинг веб сервера (Nginx, VS Code и др.)