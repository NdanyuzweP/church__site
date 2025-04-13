from django import forms
from .models import ContactMessage, PrayerRequest, Donation

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'request', 'is_private']
        widgets = {
            'request': forms.Textarea(attrs={'rows': 5}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_private': 'Keep this prayer request private (only viewable by church staff)',
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'amount', 'donation_type', 'is_recurring', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_recurring': 'Make this a recurring monthly donation',
        }