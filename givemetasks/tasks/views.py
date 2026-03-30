from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime 
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth import logout


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('dashboard')

    return render(request, 'signup.html')

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
    
    


def dashboard(request):

    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)

        total = tasks.count()
        completed = tasks.filter(completed=True).count()
        pending = tasks.filter(completed=False).count()

        # 🔥 streak logic
        streak = 0
        today = date.today()

        for i in range(0, 30):
            day = today - timedelta(days=i)
            if tasks.filter(completed=True, created__date=day).exists():
                streak += 1
            else:
                break

    else:
        # 👤 guest user
        tasks = []
        total = 0
        completed = 0
        pending = 0
        streak = 0

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
        'streak': streak
    }

    return render(request, 'dashboard.html', context)


from django.http import JsonResponse

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')

        task = Task.objects.create(
            user=request.user,
            title=title,
            priority=priority,
            due_date=due_date
        )

        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'priority': task.priority,
            'completed': task.completed
        })

    return JsonResponse({'error': 'Invalid request'})


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

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import redirect

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')