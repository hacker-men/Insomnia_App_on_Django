from django.db import models
from django.contrib.auth.models import User as AuthUser
from datetime import datetime, timedelta
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(AuthUser , on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class SleepLog(models.Model):
    """Model for tracking user's sleep history (insomnia management)."""
    user = models.ForeignKey(AuthUser , on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sleep_start_time = models.TimeField(null=True, blank=True)
    sleep_end_time = models.TimeField(null=True, blank=True)
    duration_hours = models.FloatField(null=True, blank=True, help_text="Total sleep in hours")
    quality = models.CharField(max_length=20, choices=[('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')])
    notes = models.TextField(blank=True, help_text="Any notes on sleep issues or factors")

    def save(self, *args, **kwargs):
        # Если duration не задан и есть оба времени начала и конца — вычисляем
        if (self.duration_hours is None or self.duration_hours == '') and self.sleep_start_time and self.sleep_end_time:
            # Объединяем с датой — используем date, если задана, иначе сегодня
            base_date = self.date if getattr(self, 'date', None) else timezone.localdate()
            start_dt = datetime.combine(base_date, self.sleep_start_time)
            end_dt = datetime.combine(base_date, self.sleep_end_time)
            # Если конец не позже старта — считаем, что перешли через полночь
            if end_dt <= start_dt:
                end_dt += timedelta(days=1)
            delta = end_dt - start_dt
            self.duration_hours = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.quality})"

class Tip(models.Model):
    """Static or admin-managed tips for insomnia relief."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[('relaxation', 'Relaxation'), ('routine', 'Routine'), ('environment', 'Environment')])

    def __str__(self):
        return self.title