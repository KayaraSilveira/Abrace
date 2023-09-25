
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounts.models import Category
from projects.models import Project

class ProjectCategoriesForm(ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=None, 
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-profile'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'] = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all() , 
            widget=forms.SelectMultiple(attrs={'class': 'js-choice form-control'}),
            required=False,
            label='Categorias',
        )

    class Meta:
        model = Project
        fields = [
            'categories',
        ]
        widgets = {
            'categories': forms.SelectMultiple()
        }
