from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, RelatedOnlyFieldListFilter
from .models import Task, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_default", "owner", "icon_url")
    list_filter = ("owner",)

    # Auto-assign owner if not a superuser
    def save_model(self, request, obj, form, change):
        if not obj.owner and not request.user.is_superuser:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "category", "completed_on", "created_at")
    list_filter = (
        ("user", RelatedOnlyFieldListFilter),
        ("created_at", DateFieldListFilter),
        ("completed_on", DateFieldListFilter),
    )
    search_fields = ("title",)


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
