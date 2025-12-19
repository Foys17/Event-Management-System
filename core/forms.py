from django import forms
from .models import ClientRequest, Event, Review, Sponsorship, User
from django.contrib.auth.forms import UserCreationForm

class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ['event_type', 'requirements', 'budget']
        widgets = {
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 
            'budget',  
            'description', 
            'date', 
            'location', 
            'registration_deadline', 
            'is_active'
        ]
        
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['amount', 'branding_assets']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email') 