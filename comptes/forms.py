from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Dresseur, Pokemone


class InscriptionForm(UserCreationForm):
    """Étape 1 : création du compte dresseur."""
    email = forms.EmailField(required=True, label='Adresse e-mail')

    class Meta:
        model = Dresseur
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmer le mot de passe'
        for champ in self.fields.values():
            champ.widget.attrs.update({'placeholder': champ.label})


class PokemoneForm(forms.ModelForm):
    """Étape 2 : création libre du pokémone (nom, type, image, présentation)."""

    class Meta:
        model = Pokemone
        fields = ['nom', 'type', 'modele_3d', 'image', 'presentation']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'ex. Braisor, Nymbulle, Volteck…'}),
            'type': forms.RadioSelect,
            'modele_3d': forms.RadioSelect,
            'presentation': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'ex. Attrapé un jour de pluie, jamais reparti.'
            }),
        }
        labels = {
            'nom': 'Nom du pokémone',
            'type': 'Type principal',
            'modele_3d': 'Modèle 3D (optionnel)',
            'image': 'Ou une image à toi',
            'presentation': 'Petite phrase de présentation',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modele_3d'].choices = [('', 'Aucun — utiliser une image')] + list(Pokemone._meta.get_field('modele_3d').choices)
        self.fields['modele_3d'].required = False


class ProfilForm(forms.ModelForm):
    """Modification du profil dresseur (bio)."""
    class Meta:
        model = Dresseur
        fields = ['bio']
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'Une phrase pour te présenter'}),
        }
