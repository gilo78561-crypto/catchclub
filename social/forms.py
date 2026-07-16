from django import forms
from .models import Post, Commentaire


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contenu', 'media']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'rows': 2, 'placeholder': "Quoi de neuf ? (@pseudo pour mentionner un ami)",
                'data-mention-input': '1',
            }),
        }
        labels = {'contenu': '', 'media': ''}

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('contenu') and not cleaned.get('media'):
            raise forms.ValidationError("Écris un texte ou ajoute une photo/vidéo.")
        return cleaned


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.TextInput(attrs={
                'placeholder': 'Écrire un commentaire… (@pseudo pour mentionner)',
                'data-mention-input': '1',
            }),
        }
        labels = {'contenu': ''}
