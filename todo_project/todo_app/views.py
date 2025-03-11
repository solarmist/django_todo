import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView

from .models import Task, Category
from .forms import TaskForm, RegisterForm, CategoryForm

SILLY_FORTUNES = [
    "Your next task will involve at least 7% more enthusiasm than usual!",
    "Beware of the printer. It knows too much.",
    "A wild coffee break appears! It's super effective!",
    "In the battle between you and your tasks, you are now winning 1-0!",
    "You are 100% more productive than a potato. Keep it up!",
    "The stapler sees all. Watch your back.",
    "A task a day keeps the chaos away… or so they say!",
]


def get_fortune():
    return random.choice(SILLY_FORTUNES)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        category_id = self.request.GET.get("category")
        hide_completed = self.request.GET.get("hide")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if hide_completed:
            queryset = queryset.filter(completed_on__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            owner=self.request.user
        ) | Category.objects.filter(owner__isnull=True)
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = []  # No form needed, we're just updating `completed_on`

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed_on = None if task.completed_on else timezone.now()
        task.save()
        if task.completed_on:
            fortune = get_fortune()
            messages.success(request, f"Task completed! 🔮 {fortune}")

        # Preserve filters when redirecting
        query_params = self.request.GET.urlencode()
        return HttpResponseRedirect(f"{reverse('task-list')}?{query_params}")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "add_task.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "add_category.html"
    success_url = reverse_lazy("task-list")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "add_category.html"
    success_url = reverse_lazy("task-list")  # Redirect after creation

    def form_valid(self, form):
        # If user is not a superuser, assign them as the category owner
        if not self.request.user.is_superuser:
            form.instance.owner = self.request.user
        else:
            form.instance.owner = None  # Superuser-created categories are global
        if form.cleaned_data["icon"] is None and form.cleaned_data["default_icon"]:
            form.instance.icon = f"icons/{form.cleaned_data['default_icon']}"

        return super().form_valid(form)
