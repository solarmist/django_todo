from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "completed_on"]
        widgets = {"completed_on": forms.DateInput(attrs={"type": "datetime-local"})}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 10:
            raise forms.ValidationError("Title must be at least 10 characters long.")
        return title
