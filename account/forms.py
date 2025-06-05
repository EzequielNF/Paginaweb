from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username / Email',
                                                             'class': 'login__input'}))

    password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password',
                                                             'class': 'login__input'}))