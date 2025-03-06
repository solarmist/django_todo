from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from .forms import TaskForm, RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("task-list")
        print(form.errors)

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
    tasks = Task.objects.filter(user=request.user)
    return render(request, "task_list.html", {"tasks": tasks})


@login_required
def mark_as_done(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        if task.completed_on is not None:
            task.completed_on = None
        else:
            task.completed_on = timezone.now()
        task.save()
    return redirect("task-list")


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
