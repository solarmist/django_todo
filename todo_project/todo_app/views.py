from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "task_list.html", {"tasks": tasks})


def mark_as_done(request, task_id):

    task = get_object_or_404(Task, id=task_id)
    task.completed_on = timezone.now()
    task.save()
    return redirect("task-list")


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task-list")
    else:
        form = TaskForm()
    return render(request, "add_task.html", {"form": form})
