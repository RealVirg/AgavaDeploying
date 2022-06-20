from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': "password"}), required=True)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': "repeat password"}), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "username"}),
            'firstname': forms.TextInput(attrs={'placeholder': "firstname"}),
            'email': forms.EmailInput(attrs={'placeholder': "Email"})
        }
        labels = {
            'username': '',
            'firstname': '',
            'email': ''
        }

        required = {
            "username": True,
            "email": True,
            "firstname": True
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "password"}), label='')
