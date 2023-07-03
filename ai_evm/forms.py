from django import forms
from .models import Voter, Party, Candidate

class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = '__all__'
        widgets = {
            'cnic': forms.TextInput(attrs={'class': 'form-control'}),
            'family_no': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'statical_lock_code': forms.TextInput(attrs={'class': 'form-control'}),
            'series_number': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['name', 'full_name', 'description', 'logo', 'candidate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'candidate': forms.Select(attrs={'class': 'form-control'}),
        }
class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        widgets = {
            'voter': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'voter': '',
        }