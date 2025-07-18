# Руководство по установке
Перед использованием создать файлы в папке config: main.env, bot.env и webflow.env, примеры содержимого есть в подпапке example config

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
pip install -r requirements.txt
```
### Запустить main.py

Для работы необходим хостинг веб сервера (Nginx, VS Code или др.)