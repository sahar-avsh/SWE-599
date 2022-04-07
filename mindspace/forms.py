from django import forms
from .models import (
    Mindspace,
    Resource,
    Note,
)

from django.core.exceptions import ValidationError
import magic

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
            'description',
            'res_format',
            'video',
            'image',
            'document',
            'quote',
            'link'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['res_format'].widget.attrs.update({'id': 'res_format_field'})
        self.fields['video'].widget.attrs.update({'id': 'video_field'})
        self.fields['image'].widget.attrs.update({'id': 'image_field'})
        self.fields['document'].widget.attrs.update({'id': 'document_field'})
        self.fields['document'].help_text = 'Please upload a PDF document'
        self.fields['quote'].widget.attrs.update({'id': 'quote_field'})
        self.fields['link'].widget.attrs.update({'id': 'link_field', 'placeholder': 'If the link is a video and you want to view it on your Resource page, please make sure to provide a Youtube or a Vimeo link'})

    def clean_document(self):
        file = self.cleaned_data.get('document', False)
        if file:
            filetype = magic.from_buffer(file.read())
            if not 'PDF' in filetype:
                raise ValidationError("File is not PDF.")
        return file

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
        self.fields['profile_to_share'].widget = forms.EmailInput(attrs={
            'id': 'profile_to_share_field',
            'placeholder': 'Enter an email'})
