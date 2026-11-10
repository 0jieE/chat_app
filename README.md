# Django Channels Chat App

A small real-time chat app for a seminar demo, built with Django 5 and Django Channels.
Messages are sent over WebSockets and saved to SQLite.

## Setup on Windows

Open PowerShell in the `chat_app` folder:

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database tables
python manage.py migrate

# 4. (Optional) Create an admin account for /admin/
python manage.py createsuperuser

# 5. Start the server (Daphne serves both HTTP and WebSockets)
python manage.py runserver
```

You should see `Starting ASGI/Daphne ...` in the log. Then open http://127.0.0.1:8000/,
sign up, and create or join a room. To see live chat, open the same room in a second
browser (or a private window) logged in as a different user.

> If PowerShell blocks `activate`, run
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use `venv\Scripts\activate.bat` from cmd.

## Using Redis (optional)

By default the app uses an in-memory channel layer, which works for a single server
process. To use Redis instead, start a Redis server and set `REDIS_URL` before running:

```powershell
$env:REDIS_URL = "redis://127.0.0.1:6379"
python manage.py runserver
```

## Project layout

| Path | What it does |
| --- | --- |
| `config/` | Settings, URLs, and the ASGI app that routes HTTP vs. WebSocket |
| `chat/models.py` | `Room` and `Message` models |
| `chat/views.py` | Room list, room page, and signup |
| `chat/consumers.py` | WebSocket consumer: receives, saves, and broadcasts messages |
| `chat/routing.py` | WebSocket URL: `ws/chat/<room_name>/` |
| `chat/static/chat/` | Frontend JavaScript and CSS |
| `templates/` | Base layout plus login and signup pages |
