from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Category, DEFAULT_ICONS


class CategoryForm(forms.ModelForm):
    default_icon = forms.ChoiceField(
        choices=[("", "Choose a default icon")] + DEFAULT_ICONS,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    icon = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Category
        fields = ["name", "icon", "owner"]

    def save(self, commit=True):
        category = super().save(commit=False)
        if not category.icon and self.cleaned_data["default_icon"]:
            category.icon = self.cleaned_data["default_icon"]
        if commit:
            category.save()
        return category


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "completed_on", "category"]
        exclude = ["completed_on"]  # Exclude the completed_on field
        widgets = {"completed_on": forms.DateInput(attrs={"type": "datetime-local"})}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 10:
            raise forms.ValidationError("Title must be at least 10 characters long.")
        return title
