
from collections import defaultdict
from django.forms import ModelForm
from projects.models import Comment


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'required':'required', 'placeholder': 'Escreva um Comentário...'})
        self._my_errors = defaultdict(list)

    class Meta:
        model = Comment
        fields = [
            'text',
        ]


