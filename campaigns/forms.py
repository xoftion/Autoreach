from django import forms
from .models import Campaign
import csv
import io


class CampaignForm(forms.ModelForm):
    csv_file = forms.FileField(required=False, help_text="Upload CSV with columns: email, name")
    
    class Meta:
        model = Campaign
        fields = ['name', 'subject', 'message', 'image1', 'image2', 'image3', 'send_interval_minutes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Campaign message...'}),
            'send_interval_minutes': forms.NumberInput(attrs={'class': 'form-control', 'value': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csv_file'].widget.attrs.update({'class': 'form-control'})
