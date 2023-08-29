
from collections import defaultdict
from django.forms import ModelForm
from projects.models import Post


class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'required':'required', 'placeholder': 'Escreva uma Postagem...'})
        self._my_errors = defaultdict(list)

    class Meta:
        model = Post
        fields = [
            'text',
        ]


