
from django import forms
from collections import defaultdict
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from projects.models import Project


class ProjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cover_photo'].widget.attrs.update({'class': 'form-control-file d-none', 'id': 'flImage'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'required':'required'})
        self._my_errors = defaultdict(list)

    class Meta:
        model = Project
        fields = [
            'cover_photo',
            'name',
            'description',
        ]
        labels = {
            'name': 'Nome *',
            'cover_photo': 'Imagem de capa *',
            'description': 'Descrição *',
        }



    def clean_name(self):
        data = self.cleaned_data.get('name').strip()

        if len(data) < 1:
            raise ValidationError(
                'Este campo não pode estar vazio',
                code='required',
            )

        return data

    def clean_description(self):
        data = self.cleaned_data.get('description')

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


