from django import forms

from .models import Question, Answer
from mindspace.models import *
from markdownx.widgets import MarkdownxWidget

class QuestionSearchForm(forms.ModelForm):
    keyword = forms.CharField(max_length=100)
    class Meta:
        model = Question
        fields = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['keyword'].required = True

class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'body',
            'tagged_mindspace',
            'tagged_resource'
        ]

        labels = {
            'title': 'Title',
            'body': 'Question'
        }

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={
            'id': 'title_field',
            'placeholder': 'Enter your question title'})
        self.fields['body'].widget = MarkdownxWidget(attrs={
            'id': 'body_field',
            'placeholder': 'Explain your question. You can use Markdown...'})
        self.fields['tagged_mindspace'].queryset = Mindspace.objects.filter(owner=profile)
        self.fields['tagged_resource'].queryset = Resource.objects.none()
        self.fields['tagged_mindspace'].required = False
        self.fields['tagged_resource'].required = False

        if 'tagged_mindspace' in self.data:
            try:
                mindspace_id = int(self.data.get('tagged_mindspace'))
                self.fields['tagged_resource'].queryset = Resource.objects.filter(belongs_to_id=mindspace_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.id:
            if self.instance.tagged_mindspace:
                self.fields['tagged_resource'].queryset = self.instance.tagged_mindspace.resources.order_by('title')
                self.fields['tagged_resource'].label_from_instance = lambda obj: "%s" % obj.title

class AnswerModelForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'reply',
            'tagged_mindspace',
            'tagged_resource'
        ]

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reply'].widget = MarkdownxWidget(attrs={
            'id': 'reply_field',
            'placeholder': 'Enter your reply. You can use Markdown...'})
        
        self.fields['tagged_mindspace'].widget.attrs.update({
            'id': 'id_tagged_mindspace_answer'
        })
        self.fields['tagged_resource'].widget.attrs.update({
            'id': 'id_tagged_resource_answer'
        })
        self.fields['tagged_mindspace'].queryset = Mindspace.objects.filter(owner=profile)
        self.fields['tagged_resource'].queryset = Resource.objects.none()
        self.fields['tagged_mindspace'].required = False
        self.fields['tagged_resource'].required = False

        if 'tagged_mindspace' in self.data:
            try:
                mindspace_id = int(self.data.get('tagged_mindspace'))
                self.fields['tagged_resource'].queryset = Resource.objects.filter(belongs_to_id=mindspace_id).order_by('title')
            except (ValueError, TypeError):
                pass
        elif self.instance.id:
            if self.instance.tagged_mindspace is not None:
                self.fields['tagged_resource'].queryset = self.instance.tagged_mindspace.resources.order_by('title')
                self.fields['tagged_resource'].label_from_instance = lambda obj: "%s" % obj.title