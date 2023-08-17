from django import forms


class LoginForm(forms.Form):

    email = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        error_messages={'required': 'Este campo não pode estar vazio'}
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}),
        error_messages={'required': 'Este campo não pode estar vazio'}
    )