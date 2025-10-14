from django.db import models
from django.contrib.auth.models import User as AuthUser
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(AuthUser , on_delete=models.CASCADE, verbose_name=_('User'))
    firstname = models.CharField(_("First name"),max_length=100)
    lastname = models.CharField(_("Last name"),max_length=100)
    age = models.IntegerField(_("Age"))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class SleepLog(models.Model):
    """Model for tracking user's sleep history (insomnia management)."""
    user = models.ForeignKey(AuthUser , on_delete=models.CASCADE, verbose_name=_('User'))
    date = models.DateField(_("Date"),auto_now_add=True)
    sleep_start_time = models.TimeField(_("Sleep start time"), null=True, blank=True)
    sleep_end_time = models.TimeField(_("Sleep end time"),null=True, blank=True)
    duration_hours = models.FloatField(_("Duration (hours)"), null=True, blank=True, help_text=_("Total sleep in hours"))
    quality = models.CharField(max_length=20, choices=[('good', _('Good')), ('fair', _('Fair')), ('poor', _('Poor'))])
    notes = models.TextField(_("Notes"), blank=True, help_text=_("Any notes on sleep issues or factors"))

    class Meta:
        verbose_name = _('Sleep Log')
        verbose_name_plural = _('Sleep Logs')

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
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    category = models.CharField(_("Category"), max_length=50, choices=[('relaxation', _('Relaxation')), ('routine', _('Routine')), ('environment', _('Environment'))])

    class Meta:
        verbose_name = _('Tip')
        verbose_name_plural = _('Tips')
        
    def __str__(self):
        return self.title