
from collections import defaultdict
from django.forms import ModelForm, IntegerField
from accounts.models import Review
from django import forms
from django.core.exceptions import ValidationError


class ReviewForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_body'].widget.attrs.update({'class': 'form-control', 'required' :'required', 'placeholder': 'Escreva uma avaliação...'})
        self.fields['review_value'].widget.attrs.update({'min': '1', 'max': '5'})
        self._my_errors = defaultdict(list)

    class Meta:
        model = Review
        fields = [
            'review_value',
            'review_body'
        ]
        labels = {
            'review_body': 'Texto de avaliação',
            'review_value': 'Nota'
        }


