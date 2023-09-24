
from django import forms
from collections import defaultdict
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser


class EditProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control cep-input', 'required':'required'})
        self.fields['birth_date'] = forms.DateField(
            label='Data de nascimento',
            widget=forms.DateInput(format=('%Y-%m-%d'),
                                   attrs={'class': 'form-control',
                                          'required': 'required',
                                          'type': 'date'
                                          })
        )
        
        self._my_errors = defaultdict(list)

    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            'zipcode',
            'city',
            'state',
            'country',
            'birth_date',
        ]
        labels = {
            'profile_picture': 'Foto de Perfil',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'city': 'Cidade',
            'state': 'Estado',
            'country': 'País',
            'zipcode': 'CEP',
            'birth_date': 'Data de nascimento',
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
    

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        if self._my_errors:
            raise ValidationError(self._my_errors)


