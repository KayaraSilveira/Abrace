
from collections import defaultdict
from django.forms import ModelForm, IntegerField
from accounts.models import Review


class ReviewForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_body'].widget.attrs.update({'class': 'form-control', 'required':'required', 'placeholder': 'Escreva uma avaliação...'})
        self.fields['review_value'] = IntegerField(

        )
        self._my_errors = defaultdict(list)

    class Meta:
        model = Review
        fields = [
            'review_body',
            'review_value'
        ]
        labels = {
            'review_body': 'Texto de avaliação',
            'review_value': 'Estrelas'
        }


