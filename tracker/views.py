from django.shortcuts import render
from .forms import DailyRecordForm

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # создаём нового пользователя
            return redirect('login')  # перенаправляем на страницу входа
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def calendar_view(request):
    records = DailyRecord.objects.filter(user=request.user)
    return render(request, 'calendar.html', {'records': records})


import datetime
from .models import DailyRecord
from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def entry_view(request, year, month, day):
    date = datetime.date(year, month, day)
    # Пытаемся получить существующую запись этого пользователя на указанную дату
    record = DailyRecord.objects.filter(user=request.user, date=date).first()
    if request.method == 'POST':
        # Если запись уже есть, обновляем её, иначе создаём новую
        if record:
            form = DailyRecordForm(request.POST, instance=record)
        else:
            form = DailyRecordForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user  # привязываем запись к текущему пользователю
            new_record.date = date
            new_record.save()
            return redirect('calendar')  # возвращаемся на календарь или на ту же страницу
    else:
        # GET-запрос: показываем форму. Если запись есть, заполняем её данными.
        form = DailyRecordForm(instance=record)
    return render(request, 'entry.html', {
        'form': form,
        'date': date,
        'record': record,
    })


from django.db.models import Sum

@login_required(login_url='login')
def summary_view(request):
    # Читаем параметр периода (week, month, all), по умолчанию 'all'
    period = request.GET.get('period', 'all')
    today = datetime.date.today()
    if period == 'week':
        start_date = today - datetime.timedelta(days=6)
    elif period == 'month':
        start_date = today - datetime.timedelta(days=29)
    else:
        start_date = None  # весь период
    # Фильтруем записи текущего пользователя за нужный период
    records = DailyRecord.objects.filter(user=request.user)
    if start_date:
        records = records.filter(date__gte=start_date)
    # Агрегируем суммарно часы по категориям
    totals = records.aggregate(
        total_useful=Sum('hours_useful'),
        total_doubtful=Sum('hours_doubtful'),
        total_wasted=Sum('hours_wasted')
    )
    return render(request, 'summary.html', {
        'period': period,
        'totals': totals
    })


