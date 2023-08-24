
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounts.models import CustomUser, Category


class ProfileCategoriesForm(ModelForm):

    categories = forms.ModelMultipleChoiceField(
        queryset=None, 
        label='',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-profile'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all() 

    class Meta:
        model = CustomUser
        fields = [
            'categories',
        ]
