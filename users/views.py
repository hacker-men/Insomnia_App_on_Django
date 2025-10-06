from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
from django.db.models import Count
from .models import Profile, SleepLog, Tip
from .forms import SleepLogForm

def home(request):
    """Home page - public landing for insomnia app."""
    tips = Tip.objects.all()[:3]
    context = {'tips': tips}
    return render(request, 'home.html', context)

def register(request):
    """Signup/registration view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        
        # Create user with built-in auth
        user = AuthUser.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, firstname=firstname, lastname=lastname, age=age)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):  # Renamed to avoid conflict with built-in
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    """User  dashboard - overview of profile and recent sleep."""
    profile = Profile.objects.get(user=request.user)
    recent_sleep = SleepLog.objects.filter(user=request.user).order_by('-date')[:5]
    context = {
        'profile': profile,
        'recent_sleep': recent_sleep,
    }
    return render(request, 'dashboard.html', context)

@login_required
def sleep_history(request):
    """View sleep logs/history and allow creating new logs."""
    if request.method == 'POST':
        form = SleepLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, 'Sleep log added.')
            return redirect('sleep_history')
    else:
        form = SleepLogForm()

    sleep_logs = SleepLog.objects.filter(user=request.user).order_by('-date')
    context = {'sleep_logs': sleep_logs, 'form': form}
    return render(request, 'sleep_history.html', context)

#@login_required
#def sleep_statistics(request):
#    sleep_logs = SleepLog.objects.filter(user=request.user)
#    total = sleep_logs.count()
#    if total:
#        # защищённый суммирование: пропускаем None
#        durations = [log.duration_hours for log in sleep_logs if log.duration_hours is not None]
#        avg_duration = round(sum(durations) / len(durations), 2) if durations else 0
#        # Если в модели есть QUALITY_CHOICES, используйте их; иначе извлеките уникальные значения
#        try:
#            choices = SleepLog._meta.get_field('quality').choices
#        except Exception:
    #         choices = []
    #     quality_counts = {}
    #     if choices:
    #         for key, _label in choices:
    #             quality_counts[key] = sleep_logs.filter(quality=key).count()
    #     else:
    #         # fallback — все существующие значения
    #         for q, cnt in sleep_logs.values_list('quality', flat=True).distinct().annotate(count=models.Count('quality')):
    #             pass
    #         # проще: use values/annotate
    #         from django.db.models import Count
    #         qc = sleep_logs.values('quality').annotate(count=Count('quality'))
    #         quality_counts = {item['quality']: item['count'] for item in qc}
    # else:
    #     avg_duration = 0
    #     quality_counts = {}

#    context = {
#        'avg_duration': avg_duration,
#        'quality_counts': quality_counts,
#        'total_logs': total,
#    }
#    return render(request, 'sleep_statistics.html', context)

@login_required
def tips(request):
    """Insomnia tips page."""
    all_tips = Tip.objects.all()
    context = {'tips': all_tips}
    return render(request, 'tips.html', context)

@login_required
def logout_view(request):
    """Logout and redirect to home."""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')