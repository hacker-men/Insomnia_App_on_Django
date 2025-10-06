from django import forms
from .models import SleepLog

class SleepLogForm(forms.ModelForm):
    class Meta:
        model = SleepLog
        fields = ['date', 'sleep_start_time', 'sleep_end_time', 'duration_hours', 'quality', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sleep_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sleep_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'step': '0.25', 'class': 'form-control'}),
            'quality': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
