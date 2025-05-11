from django import forms
from .models import DailyRecord

class DailyRecordForm(forms.ModelForm):
    class Meta:
        model = DailyRecord
        fields = ['hours_useful', 'hours_doubtful', 'hours_wasted', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
