from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending
    }

    return render(request, 'dashboard.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            user=request.user,
            title=title,
            priority=priority,
            due_date=due_date
        )

    return redirect('dashboard')


@login_required
def complete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')


@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('dashboard')