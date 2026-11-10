from django.contrib import admin
from django.urls import include, path

from chat import views as chat_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Signup lives next to Django's built-in auth URLs (login, logout, ...).
    # It's declared here so it can't be mistaken for a chat room name.
    path("accounts/signup/", chat_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("chat.urls")),
]
