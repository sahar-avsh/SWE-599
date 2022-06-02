from django import forms
from .models import (
    Mindspace,
    Resource,
    Note,
    ShareMindspace,
)

from django.core.exceptions import ValidationError
import magic

from django.forms.models import BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME

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
            'content'
        ]

class MindspaceSearchForm(forms.Form):
    keyword = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'id-search-keyword',
        'class': 'search-keyword',
        'placeholder': 'Search by keyword'
    }), required=False)
    owner = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'id-search-owner',
        'class': 'search-owner',
        'placeholder': 'Search by username'
    }), required=False)


class ShareMindspaceModelForm(forms.ModelForm):
    # shared_with_info = forms.EmailField()
    class Meta:
        model = ShareMindspace
        fields = [
            'access_level',
            'shared_with_info'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shared_with_info'].widget = forms.TextInput(attrs={
            'id': 'id-shared-with-info',
            'placeholder': 'Enter a valid email or username'})
        self.fields['shared_with_info'].label = 'Share with'


class BaseShareMindspaceModelFormSet(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseShareMindspaceModelFormSet, self).add_fields(form, index)
        if DELETION_FIELD_NAME in form.fields.keys():
            form.fields[DELETION_FIELD_NAME].label = 'Remove access'

ShareMindspaceModelFormSet = forms.modelformset_factory(ShareMindspace, form=ShareMindspaceModelForm, formset=BaseShareMindspaceModelFormSet, extra=1, can_delete=True, can_delete_extra=False)

