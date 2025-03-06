from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("tasks/", include("todo_app.urls")),
    path("admin/", admin.site.urls),
]
