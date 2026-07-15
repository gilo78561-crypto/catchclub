from django import forms
from .models import Post, Commentaire


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contenu', 'image']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Quoi de neuf ?'}),
        }
        labels = {'contenu': '', 'image': ''}


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.TextInput(attrs={'placeholder': 'Écrire un commentaire…'}),
        }
        labels = {'contenu': ''}
