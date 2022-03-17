from django import forms
from .models import Mindspace

class MindspaceModelForm(forms.ModelForm):
    class Meta:
        model = Mindspace
        fields = [
            'title',
            'description'
        ]