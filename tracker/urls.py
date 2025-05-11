from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),          # главная
    path('register/', views.register, name='register'),
    path('entry/<int:year>-<int:month>-<int:day>/',
         views.entry_view, name='entry'),
    path('summary/', views.summary_view, name='summary'),
]
