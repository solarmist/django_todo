from django.urls import path, include

urlpatterns = [
    path("tasks/", include("todo_app.urls")),
]
