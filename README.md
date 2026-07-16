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

## 10. Nouveautés (recherche, pièces jointes, réponses, échanges visibles)

- **Recherche fonctionnelle** : la barre du header cherche maintenant
  vraiment les dresseurs (par pseudo ou nom de pokémone) et les groupes.
- **Messagerie** : possibilité d'envoyer une image ou une vidéo (bouton 📎),
  affichées directement dans les bulles de conversation. Le pokémon de
  l'interlocuteur (nom, type, modèle 3D si disponible) est visible en haut
  du chat, et un bouton **"🔁 Échanger une carte"** y donne un accès direct.
- **Échange de cartes** : bouton dédié maintenant visible aussi bien sur
  le profil d'un ami que dans sa conversation (avant, il fallait deviner
  l'URL).
- **Réponses aux commentaires** : chaque commentaire a un bouton
  "Répondre" qui ouvre un petit formulaire ; les réponses s'affichent
  indentées sous le commentaire d'origine (un seul niveau de profondeur).

## 12. Adaptation mobile

Le site est maintenant réactif sur petit écran (téléphone) :
- l'en-tête (logo, recherche, icônes) s'empile proprement au lieu de déborder,
- la messagerie passe en une colonne (liste des conversations au-dessus,
  fenêtre de chat en dessous),
- l'écran d'échange de cartes passe ses deux colonnes en pile,
- les grilles (collection, sélecteurs de type/modèle 3D) s'adaptent à la
  largeur disponible.

Le point de rupture principal est à 640px de large (téléphones), avec un
second à 1020px déjà présent pour les tablettes (les 3 colonnes du fil
d'actualité passent alors à 1 colonne).

## 14. Installer CatchClub comme une application (PWA)

Le site est maintenant une **Progressive Web App** : il peut s'installer
sur téléphone (ou PC) avec sa propre icône, et s'ouvrir en plein écran
sans barre d'adresse, comme une vraie application.

**Sur Android (Chrome)** : ouvrir le site, menu ⋮ → **"Installer
l'application"** (ou un bandeau propose de le faire automatiquement).

**Sur iPhone (Safari)** : ouvrir le site, bouton **Partager** (carré avec
flèche) → **"Sur l'écran d'accueil"**.

**Sur PC (Chrome/Edge)** : une icône ⊕ apparaît dans la barre d'adresse
pour installer le site comme application de bureau.

Ce que ça ajoute techniquement :
- `static/manifest.json` : nom, icônes, couleurs, mode plein écran
  (`display: standalone`).
- `static/icons/` : icônes générées aux formats nécessaires (192px, 512px,
  icône Apple, favicon).
- `static/sw.js` (service worker), servi depuis la racine du site
  (`/sw.js`, voir `config/urls.py`) pour qu'il couvre bien tout le site.
  Il met en cache la feuille de style et les icônes pour un chargement
  plus rapide, et garde en mémoire les dernières pages visitées pour un
  minimum de contenu accessible hors-ligne. Les modèles 3D (trop lourds)
  ne sont volontairement pas mis en cache.

Ça ne remplace pas une vraie application native (pas de notifications
push, par exemple), mais ça donne l'expérience "icône + plein écran" que
tu voulais, sans code supplémentaire côté utilisateur.

## 16. Notifications

La cloche 🔔 du header (jusque-là décorative) est maintenant fonctionnelle :
un point rouge apparaît quand il y a du nouveau, et la page
`/notifications/` liste les événements qui te concernent — nouvel
abonné, like, commentaire (ou réponse à ton commentaire), proposition
d'échange reçue, échange accepté/refusé. Ouvrir la page marque tout
comme lu. Ce sont des notifications **dans le site** (pas des
notifications push qui arrivent même site fermé — ça demanderait une
mise en place différente, dis-le-moi si c'est ce dont tu as besoin).

## 17. Correctif important — bug d'affichage mobile

Les essais précédents d'adaptation mobile ne s'appliquaient pas
vraiment : les règles CSS étaient placées trop tôt dans le fichier
`style.css`, avant les styles de base qu'elles étaient censées
corriger — en CSS, à règle "aussi précise", c'est toujours la dernière
déclarée dans le fichier qui l'emporte. Tout le bloc mobile a été
déplacé à la toute fin du fichier, ce qui corrige l'affichage sur
téléphone pour toutes les pages (groupes, collection, échange,
messagerie, mon pokémon...).

## 19. Photos et vidéos dans les publications

Le composer du fil d'actualité a maintenant un bouton 📷 pour joindre une
photo **ou** une vidéo à une publication (en plus ou à la place du texte).
Comme pour la messagerie, un post peut être : texte seul, média seul, ou
les deux — mais pas vide. Affichage automatique en `<img>` ou `<video>`
selon le type de fichier envoyé.

## 21. Mentions "@pseudo"

Dans le composer d'un post, un commentaire ou une réponse, taper `@` suivi
de quelques lettres fait apparaître une liste de dresseurs à cliquer pour
compléter automatiquement (autocomplétion en JS pur, `social/views.py` →
`suggestions_mention`). Une fois publié :
- le `@pseudo` devient un **lien cliquable** vers le profil mentionné
  (rendu par le filtre de template `|mentions`, `social/templatetags/`),
- le dresseur mentionné reçoit une **notification** ("X t'a mentionné
  dans une publication/commentaire"), sauf s'il est déjà notifié pour la
  même action (auteur du post, du commentaire parent...).

⚠️ **Limite actuelle** : les mentions fonctionnent dans le fil principal
(posts et commentaires). Les groupes n'ont pour l'instant pas leur propre
mur de publications séparé (juste une liste de membres) — si tu veux que
chaque groupe ait son propre fil où mentionner ses membres, dis-le-moi,
c'est une fonctionnalité à part entière à construire.

## 22. Prochaines pistes (non incluses)

- Notifications en temps réel (WebSocket / Django Channels).
- Recherche réelle (actuellement la barre de recherche est visuelle).
- Upload d'images optimisé / recadrage des avatars.
- Pagination du fil d'actualité et de la collection.

Dis-moi ce que tu veux ajouter ou ajuster en premier.
