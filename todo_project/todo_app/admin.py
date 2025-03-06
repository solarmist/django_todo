from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, RelatedOnlyFieldListFilter
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "completed_on", "created_at")
    list_filter = (
        ("user", RelatedOnlyFieldListFilter),
        ("created_at", DateFieldListFilter),
        ("completed_on", DateFieldListFilter),
    )
    search_fields = ("title",)


admin.site.register(Task, TaskAdmin)
