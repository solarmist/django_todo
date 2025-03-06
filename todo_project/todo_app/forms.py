from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


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
