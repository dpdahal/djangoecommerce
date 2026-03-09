from django import forms
from .models import Contact
import re 


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }

        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'subject': 'Subject',
            'message': 'Your Message',
        }

        error_messages = {
            'name': {
                'required': 'Please enter your name.',
            },
            'email': {
                'required': 'Please enter your email address.',
            },
            'phone': {
                'required': 'Please enter your phone number.',
            },
            'subject': {
                'required': 'Please enter a subject.',
            },
            'message': {
                'required': 'Please enter your message.',
            },
        }


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        name_pattern = re.compile(r'^[a-zA-Z\s]+$')
        if not name_pattern.match(name):
            raise forms.ValidationError("Name must contain only letters and spaces.")
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
        if not email_pattern.match(email):
            raise forms.ValidationError("Enter a valid email address.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone