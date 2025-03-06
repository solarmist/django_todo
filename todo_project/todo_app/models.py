from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
