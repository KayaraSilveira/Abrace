
from collections import defaultdict
from django.forms import ModelForm
from accounts.models import Review


class ReviewForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'required':'required', 'placeholder': 'Escreva uma avaliação...'})
        self._my_errors = defaultdict(list)

    class Meta:
        model = Review
        fields = [
            'text',
        ]


