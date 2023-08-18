
from django import forms
from collections import defaultdict
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser


class RegisterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs.update({'class': 'form-control cpf-input', 'required':'required'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['password'] = forms.CharField(
            label='Senha *',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'})
        )
        self._my_errors = defaultdict(list)

    class Meta:
        model = CustomUser
        fields = [
            'cpf',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'cpf': 'cpf *',
            'first_name': 'Nome *',
            'last_name': 'Sobrenome *',
            'email': 'E-mail *',
            'password': 'Senha *'
        }



    def clean_first_name(self):
        data = self.cleaned_data.get('first_name').strip()

        if len(data) < 1:
            raise ValidationError(
                'Este campo não pode estar vazio',
                code='required',
            )

        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name').strip()

        if len(data) < 1:
            raise ValidationError(
                'Este campo não pode estar vazio',
                code='required',
            )

        return data

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if len(data) < 8:
            raise ValidationError(
                'A senha é muito curta. Digite pelo menos 8 caracteres',
                code='min-length',
            )

        return data

    def clean_email(self):
        data = self.cleaned_data.get('email', '')
        exists = CustomUser.objects.filter(email=data).exists()

        if exists:
            raise ValidationError(
                'Já existe uma conta vinculada a este E-mail', code='unique',
            )

        return data
    
    def clean_cpf(self):
        data = self.cleaned_data.get('cpf', '')
        exists = CustomUser.objects.filter(cpf=data).exists()

        if exists:
            raise ValidationError(
                'Já existe uma conta vinculada a este cpf', code='unique',
            )

        return data

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        if self._my_errors:
            raise ValidationError(self._my_errors)

