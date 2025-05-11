from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class DailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь-владелец записи
    date = models.DateField(verbose_name="Дата")
    hours_useful = models.PositiveIntegerField(verbose_name="Полезно (часов)")
    hours_doubtful = models.PositiveIntegerField(verbose_name="Сомнительно (часов)")
    hours_wasted = models.PositiveIntegerField(verbose_name="В никуда (часов)")
    notes = models.TextField(blank=True, verbose_name="Заметки")

    def __str__(self):
        return f"{self.user.username} - {self.date}"
