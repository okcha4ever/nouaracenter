from django import forms
from .models import Post, Comment

# My Forms
class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(PostForm, self).__init__(*args, **kwargs)
       self.fields['uploader'].widget.attrs['readonly'] = True

    class Meta:
        model = Post
        fields = ('image', 'uploader', 'description')
        labels = {
            'image': '', 
            'uploader': '',
            'description': '',
        }

        widgets = {

            'uploader': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'موضوع المنشور'}),
        }

class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
       super(CommentForm, self).__init__(*args, **kwargs)
       self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Comment
        fields = ('name', 'body')
        labels = {
            'name': '', 
            'body': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'موضوع التعليق'}),
        }