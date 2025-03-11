import random
from urllib.parse import urlencode

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

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


def register(request):
    if request.method == "POST":
        register = RegisterForm(request.POST)
        if register.is_valid():
            register.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("task-list")
        print(register.errors)

    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("task-list")
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def task_list(request):
    category = Category.objects.filter(name=request.GET.get("category")).first()
    hide_completed = request.GET.get("hide") == "on"
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.all()

    # Apply category filter
    if category is not None:
        tasks = tasks.filter(category=category)

    # Apply completed filter
    if hide_completed:
        tasks = tasks.filter(completed_on__isnull=True)

    return render(
        request,
        "task_list.html",
        {"tasks": tasks, "categories": categories},
    )


@login_required
def mark_as_done(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed_on = timezone.now() if task.completed_on is None else None
        task.save()
        if task.completed_on:
            fortune = get_fortune()
            messages.success(request, f"Task completed! 🔮 {fortune}")

    # Preserve filters from the request
    query_params = request.GET.copy()  # Get existing query parameters
    query_string = urlencode(query_params)  # Convert to URL format
    return redirect(f"{reverse('task-list')}?{query_string}")


@login_required
def add_task(request):
    if request.method == "POST":
        task = TaskForm(request.POST)
        task.instance.user = request.user
        if task.is_valid():
            task.save()
            return redirect("task-list")
        print(task.errors)

    form = TaskForm()
    return render(request, "add_task.html", {"form": form})


@login_required
def add_category(request):
    if request.method == "POST":
        category = CategoryForm(request.POST, request.FILES)
        # Superusers can create sitewide categories
        category.instance.owner = None if request.user.is_superuser else request.user

        if category.is_valid():
            category.save()
            return redirect("task-list")
        print(category.errors)

    form = CategoryForm()
    return render(request, "add_category.html", {"form": form})
