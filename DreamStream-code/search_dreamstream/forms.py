from django import forms
from django.forms import ModelForm
from .models import *

class TitleForm(forms.ModelForm):
    class Meta:
        model = TitleSearch
        fields = '__all__'