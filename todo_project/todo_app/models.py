from pathlib import Path
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify


# Define default icons as choices
DEFAULT_ICONS = [
    ("icon_1.png", "Icon 1"),
    ("icon_2.png", "Icon 2"),
    ("icon_3.png", "Icon 3"),
    ("icon_4.png", "Icon 4"),
    ("icon_5.png", "Icon 5"),
    ("icon_6.png", "Icon 6"),
    ("icon_7.png", "Icon 7"),
    ("icon_8.png", "Icon 8"),
    ("icon_9.png", "Icon 9"),
    ("icon_10.png", "Icon 10"),
    ("icon_11.png", "Icon 11"),
    ("icon_12.png", "Icon 12"),
    ("icon_13.png", "Icon 13"),
    ("icon_14.png", "Icon 14"),
    ("icon_15.png", "Icon 15"),
    ("icon_16.png", "Icon 16"),
]


def upload_to_category_icons(instance, filename):
    if filename.startswith("static/"):
        return filename
    file_path = Path(filename)
    short_name = slugify(file_path.stem)[:20]  # Limit filename length to 20 characters
    return f"{short_name}{file_path.suffix}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(
        upload_to=upload_to_category_icons,
        null=True,
        blank=True,
        help_text="Upload an icon or choose a default below",
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Defaults have no owner

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def icon_url(self):
        if self.icon:
            return self.icon.url
        return ""

    def is_default(self):
        return self.owner is None  # Categories without an owner are default

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} - {self.user} => {self.completed_on}"
