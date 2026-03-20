from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime 
from datetime import date, timedelta



@login_required 
def progress(request):
    tasks = Task.objects.filter(user=request.user, completed=True)
    
    # Group by date 
    data = (
        tasks 
        .extra({'date': "date(created)"})
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    dates = [str(item['date']) for item in data]
    counts = [item['count'] for item in data]
    
    context = {
        'dates': dates,
        'counts': counts
        
    }
    return render(request, 'progress.html', context)
    
    
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()

    # Streak Logic 
    
    streak = 0
    today = date.today()
    
    for i in range(0, 30):
        day = today - timedelta(days= i)
        if tasks.filter(completed = True, created__date = day).exists():
            streak += 1
        else:
            break
            
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

