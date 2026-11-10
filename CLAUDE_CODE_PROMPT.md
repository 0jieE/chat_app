# Prompt for Claude Code

Paste everything below the line into Claude Code, opened in this `chat_app` folder.

---

This is a Django 5 + Django Channels real-time chat app. The project is already scaffolded: `config/` (settings, urls, asgi, wsgi) is fully wired, and everything in `chat/` and `templates/` is a stub marked with `TODO` comments. Read the whole project first, then implement every TODO so the app runs end to end. Do not change the folder structure.

**Requirements**

1. **Models** (`chat/models.py`)
   - `Room`: `name` (unique SlugField), `created_at`.
   - `Message`: `room` (FK Room, related_name="messages"), `user` (FK AUTH_USER_MODEL), `content` (TextField), `created_at` (auto_now_add). Order by `created_at`.
   - Register both in `chat/admin.py` with useful `list_display`.

2. **Auth**
   - Use Django's built-in auth (`accounts/` URLs are already included).
   - Complete `templates/registration/login.html`.
   - Add a simple signup view + template using `UserCreationForm`, logging the user in after signup.
   - Navbar in `base.html`: show the username and a logout button (POST form, since Django 5 requires POST for logout).

3. **Views / templates**
   - `index`: list all rooms and provide a form to create or join a room by name (slugify the input), then redirect to the room.
   - `room`: `get_or_create` the room and pass the last 50 messages to the template.
   - `room.html`: render the message history, then live messages below it.

4. **WebSocket consumer** (`chat/consumers.py`)
   - Close the connection for anonymous users.
   - Join/leave the group `chat_<room_name>`.
   - On receive: validate non-empty content (max 1000 chars), save the `Message` using `database_sync_to_async`, then `group_send` with type `chat.message` and the fields username, content, and timestamp (ISO format).
   - `chat_message`: forward those fields to the client as JSON.

5. **Frontend** (`chat/static/chat/js/room.js`, `style.css`)
   - Connect to `ws://` or `wss://` based on `location.protocol`.
   - Send on button click and on Enter; clear the input after sending.
   - Append messages as "username: content · time" and auto-scroll to the bottom.
   - Show a "Disconnected" notice if the socket closes.
   - Use clean, simple CSS: a centered chat box, a scrollable log, and the user's own messages aligned right.
   - Escape message text (use `textContent`, never `innerHTML`).

6. **Finish**
   - Run `makemigrations` and `migrate`.
   - Write a short `README.md` with Windows setup steps (venv, pip install, migrate, createsuperuser, runserver).
   - Verify `python manage.py check` passes and that the server starts with Daphne (the startup log should say "Starting ASGI/Daphne").

**Constraints**
- Keep the in-memory channel layer as the default. The Redis toggle via `REDIS_URL` in settings must keep working.
- No extra packages beyond `requirements.txt`.
- Keep the code simple and well commented. This is for a seminar demo.
