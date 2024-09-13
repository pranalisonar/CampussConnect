from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, SendEmail, contactForm
from django import forms

class contact_form(forms.ModelForm):
    class Meta:
        model = contactForm
        fields = ['content']

class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = ['email_subject', 'body']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email already exist...')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_resume', 'current_status', 'user_image', 'Web_url', 'Github_url', 'Linkedin_url', 'Insta_url', 'Fb_url']