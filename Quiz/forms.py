from django import forms
from Quiz.models import User
from django.forms import PasswordInput
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username', }),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name', }),
            # 'password': forms.TextInput(attrs={'placeholder': 'Enter Password', }),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})


class UserLoginForm(forms.ModelForm):

    name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = (
            'username',
            # 'name',
            'password'
        )
        exclude = ("name",)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username', 'required': 'True'}),
            # 'name': forms.TextInput(attrs={'placeholder': 'Enter Name',  'required': 'False'}),
            'password': forms.TextInput(attrs={'placeholder': 'Enter Password', 'required': 'True'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})
