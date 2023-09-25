
from django import forms
from collections import defaultdict
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from datetime import date, timedelta

#testa o cpf
def testaCPF(strCPF):
      # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(strCPF[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(strCPF[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verifica se os dígitos verificadores calculados correspondem aos dígitos reais
    if int(strCPF[9]) == digito1 and int(strCPF[10]) == digito2:
        return True
    else:
        return False
    
class RegisterForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file d-none', 'required':'required', 'id': 'flImage'})
        self.fields['cpf'].widget.attrs.update({'class': 'form-control cpf-input', 'required':'required'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control cep-input', 'required':'required'})
        self.fields['birth_date'] = forms.DateField(
            label='Data de nascimento *',
            widget=forms.DateInput(format=('%Y-%m-%d'),
                                   attrs={'class': 'form-control',
                                          'required': 'required',
                                          'type': 'date'
                                          })
        )

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['password'] = forms.CharField(
            label='Senha *',
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'})
        )
        self._my_errors = defaultdict(list)

    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'cpf',
            'first_name',
            'last_name',
            'zipcode',
            'city',
            'state',
            'country',
            'birth_date',
            'email',
            'password',
        ]
        labels = {
            'profile_picture': 'Foto de Perfil',
            'cpf': 'cpf *',
            'first_name': 'Nome *',
            'last_name': 'Sobrenome *',
            'city': 'Cidade *',
            'state': 'Estado *',
            'country': 'País *',
            'zipcode': 'CEP *',
            'birth_date': 'Data de nascimento *',
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
        cpfLimpo = data.replace('-', '')
        cpfLimpo = cpfLimpo.replace('.', '')
        
        if not testaCPF(cpfLimpo):
            raise ValidationError('CPF inválido. Confira o CPF digitado.')
        if exists:
            raise ValidationError(
                'Já existe uma conta vinculada a este cpf', code='unique',
            )

        return data
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        min_birth_date = date.today() - timedelta(days=150*365)  

        if birth_date >= date.today() or birth_date <= min_birth_date:
            raise ValidationError(
                'Digite uma data de nascimento válida.',
                code='invalid',
            )

        return birth_date



    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        if self._my_errors:
            raise ValidationError(self._my_errors)


