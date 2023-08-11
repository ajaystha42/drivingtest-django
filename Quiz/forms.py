from django import forms
from django.contrib.auth.models import User
# from Quiz.models import User
from django.forms import PasswordInput
from django.contrib.auth.forms import AuthenticationForm


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
            'email': forms.TextInput(attrs={'placeholder': 'Enter Email', }),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})


class UserLoginForm(forms.Form):

    email = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    # class Meta:
    #     model = User
    #     fields = (
    #         'username',
    #         'email',
    #         'password'
    #     )
    #     exclude = ("email",)
    #     widgets = {
    #         'username': forms.TextInput(attrs={'placeholder': 'Enter Username', 'required': 'True'}),
    #         # 'email': forms.TextInput(attrs={'placeholder': 'Enter Name',  'required': 'False'}),
    #         'password': forms.TextInput(attrs={'placeholder': 'Enter Password', 'required': 'True'}),
    #     }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super(UserLoginForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = False

        self.fields['username'].widget.attrs.update(
            {'class': 'form-email', 'placeholder': 'Enter Username'})
        self.fields['password'].widget = PasswordInput(
            attrs={'placeholder': 'Enter Password'})
