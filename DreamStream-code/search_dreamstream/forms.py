from django import forms
from django.forms import ModelForm
from .models import *

class TitleForm(forms.ModelForm):
    search = forms.CharField(label='search', widget=forms.TextInput(attrs={'placeholder': " Search a Title"}))
    class Meta:
        model = TitleSearch
        fields = '__all__'
        