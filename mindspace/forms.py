from django import forms
from .models import (
    Mindspace,
    Resource,
)

class MindspaceModelForm(forms.ModelForm):
    class Meta:
        model = Mindspace
        fields = [
            'title',
            'description'
        ]

class ResourceModelForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'title',
            'description'
        ]