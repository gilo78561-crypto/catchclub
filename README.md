# CatchClub — Projet Django

Réseau social pour dresseurs et fans de Pokémon. Chaque dresseur crée
librement son **pokémone** à l'inscription (nom, type, image), publie
dans un fil d'actualité, s'abonne à d'autres dresseurs (ce qui débloque
automatiquement leur carte dans sa **collection**), échange des cartes,
rejoint des **groupes** par type, et discute en **messagerie privée**.

La base de données livrée (`db.sqlite3`) est déjà migrée et peuplée de
données de démonstration : tu peux lancer le site tout de suite.

---

## 1. Installation (Windows / PowerShell)

Prérequis : Python 3.11+ installé (coche "Add Python to PATH" pendant
l'installation, puis vérifie avec `python --version`).

Dans PowerShell, place-toi dans le dossier du projet puis :

```powershell
# Créer et activer un environnement virtuel
python -m venv venv
venv\Scripts\Activate.ps1

# Installer Django
pip install -r requirements.txt

# Lancer le serveur (la base est déjà prête)
python manage.py runserver
```

Si PowerShell refuse d'activer l'environnement (erreur "script désactivé"),
lance une fois : `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`,
puis réessaie `venv\Scripts\Activate.ps1`.

Ouvre ensuite **http://127.0.0.1:8000/** dans ton navigateur.

---

## 2. Comptes de démonstration

| Rôle | Identifiant | Mot de passe | Accès |
|---|---|---|---|
| Administrateur complet | `admin` | `admin1234` | `/admin/` — tous les droits |
| Modérateur (staff, pas superuser) | `modo` | `moderateur123` | `/admin/` — uniquement les **abonnements** (voir section 3) |
| Dresseur classique | `Gilo`, `Aika`, `Ryu`, `Meji`, `Loran`, `MysteLia`, `Braisor_exe` | `motdepasse123` | Le site public |

---

## 3. Droits de l'administrateur sur les abonnés

C'est le point clé demandé : l'administrateur a des **droits complets sur
les abonnements** (qui suit qui) depuis le panneau `/admin/` :

- **Consultation** : liste de tous les abonnements, avec recherche par
  dresseur et filtre par date (`Social → Abonnements`).
- **Suppression individuelle ou en masse** : une action « Forcer la
  suppression des abonnements sélectionnés (modération) » permet de
  couper un ou plusieurs abonnements abusifs en un clic.
- **Ajout/modification manuelle** possible directement depuis l'admin.

Ces droits ne sont pas réservés au superutilisateur : ils sont portés par
un **groupe Django "Modérateurs"**, créé automatiquement par la commande
`seed_demo` (voir plus bas), avec les permissions `add`/`change`/`delete`/
`view` sur le modèle `Abonnement`. N'importe quel compte `is_staff=True`
ajouté à ce groupe hérite de ces droits — c'est le cas du compte `modo`
ci-dessus, qui peut gérer les abonnements mais n'a accès à rien d'autre
dans l'admin (les dresseurs, posts, groupes, etc. restent réservés au
superutilisateur `admin`).

Pour donner ces droits à un compte existant sans repartir de zéro :
`Admin → Authentification et autorisation → Groupes → Modérateurs`,
puis ajoute le dresseur voulu à ce groupe et coche `is_staff` sur sa fiche.

---

## 4. Repartir d'une base vide

Si tu préfères repartir sans les données de démonstration :

```powershell
# Supprimer la base fournie
del db.sqlite3

# Recréer les tables
python manage.py migrate

# Créer ton propre compte administrateur
python manage.py createsuperuser

# (optionnel) recharger les données de démo, y compris le groupe Modérateurs
python manage.py seed_demo
```

`seed_demo` peut être relancée sans risque : elle ne duplique rien
(`get_or_create` partout) et remet toujours à jour les permissions du
groupe "Modérateurs".

---

## 5. Structure du projet

```
config/            réglages du projet (settings, urls)
comptes/           Dresseur (utilisateur), Pokemone, inscription 2 étapes
social/            Post, Commentaire, Abonnement, fil d'actualité
groupes/           Groupe, Adhesion — communautés par type
collection/        PossessionCarte, Echange — album + échanges de cartes
messagerie/        Conversation, Message — messagerie privée
templates/         gabarits HTML (reprennent le design de la maquette)
static/css/        feuille de style partagée
```

## 6. Fonctionnalités principales

- **Inscription en 2 étapes** : compte (`/comptes/inscription/`) puis
  création libre du pokémone (`/comptes/inscription/pokemon/`).
- **Fil d'actualité** : publications, likes, commentaires, filtré sur les
  dresseurs suivis.
- **Abonnements** : suivre un dresseur débloque automatiquement la carte
  de son pokémone dans ta collection (signal Django, `collection/signals.py`).
- **Groupes** : parcours par type de pokémon, adhésion/désadhésion.
- **Collection & échanges** : album de cartes, proposition d'échange entre
  dresseurs, acceptation/refus qui transfère réellement la propriété des
  cartes.
- **Messagerie privée** : conversations et messages en temps différé.

## 7. Modèles 3D

Cinq apparences 3D (`.glb`) sont proposées à la création (ou modification)
du pokémone, en plus de l'image classique : **Raccoony**, **Rouage**,
**Planétin**, **Astrelin**, **Ailune**. Les fichiers sont dans
`static/models/pokemon/` et affichés via le composant web
[`<model-viewer>`](https://modelviewer.dev/) (chargé depuis un CDN dans
`templates/base.html`) — rotation automatique et zoom à la souris sur la
carte dresseur du profil. Si aucun modèle 3D n'est choisi, l'image classique
(ou le cercle de type par défaut) est utilisée à la place.

Pour ajouter d'autres modèles : dépose le `.glb` dans
`static/models/pokemon/`, puis ajoute une entrée dans `MODELES_3D` et
`MODELES_3D_FICHIERS` en haut de `comptes/models.py`.

## 8. Interagir avec son pokémon

Depuis le header (icône 🎮) ou son profil, chaque dresseur accède à
**"Mon pokémon"** : le modèle 3D en grand (glisser pour tourner autour, si
un modèle 3D a été choisi), avec trois actions — **Nourrir**, **Jouer**,
**Câliner**. Chaque action :

- envoie une requête AJAX (`comptes:interagir`) qui augmente l'affection
  du pokémone en base de données (`Pokemone.affection`),
- déclenche une petite animation CSS (rebond, pulsation ou balancement)
  sur le cadre du modèle 3D — les fichiers `.glb` fournis n'ont pas
  d'animations squelettiques intégrées, donc l'interaction est simulée
  côté client plutôt que jouée depuis le modèle,
- met à jour en direct le niveau (`Pokemone.niveau`, calculé automatiquement
  tous les 50 points d'affection) et la barre de progression, sans recharger
  la page.

## 9. Déployer une version de test en ligne

Pour obtenir un lien à envoyer à des amis (hébergement gratuit, sans carte
bancaire, via Render) : voir **`DEPLOIEMENT.md`**, qui détaille toutes les
étapes pas à pas.

## 10. Prochaines pistes (non incluses)

- Notifications en temps réel (WebSocket / Django Channels).
- Recherche réelle (actuellement la barre de recherche est visuelle).
- Upload d'images optimisé / recadrage des avatars.
- Pagination du fil d'actualité et de la collection.

Dis-moi ce que tu veux ajouter ou ajuster en premier.
