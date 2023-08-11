from django import forms
from django.contrib.auth.models import User

from django.forms import PasswordInput


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username', }),
            'email': forms.TextInput(attrs={'placeholder': 'Enter Email', 'required': True, 'type': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})


class UserLoginForm(forms.Form):

    email = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-email', 'placeholder': 'Enter Username'},)
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})
