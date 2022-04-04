from django import forms
from .models import (
    Mindspace,
    Resource,
    Note,
)

class MindspaceModelForm(forms.ModelForm):
    class Meta:
        model = Mindspace
        fields = [
            'title',
            'description',
            'is_public'
        ]

        labels = {
            'is_public': 'Public'
        }

class ResourceModelForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'title',
            'description'
        ]

class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'description',
            'content'
        ]

class ShareMindspaceForm(forms.Form):
    profile_to_share = forms.EmailField(required=True)

    ACCESS_LEVELS = (
        ('viewer','VIEW'),
        ('editor', 'EDIT'),
        ('commenter', 'COMMENT')
    )

    access_level = forms.ChoiceField(choices=ACCESS_LEVELS, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_to_share'].widget = forms.TextInput(attrs={
            'id': 'profile_to_share_field',
            'placeholder': 'Enter an email'})
