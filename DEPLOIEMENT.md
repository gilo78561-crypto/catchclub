# Déployer CatchClub sur Render (pour tester avec des amis)

Ce guide t'emmène de "j'ai le projet sur mon PC" à "j'ai un lien à envoyer
à mes amis", avec **Render** (hébergement gratuit, sans carte bancaire).

⚠️ **Important à savoir avant de commencer** — le tarif gratuit de Render :
- **se met en veille après 15 minutes sans visite** : le premier clic d'un
  ami après une pause fait patienter ~30-60 secondes le temps que le site
  se réveille. Rien de cassé, juste un peu de patience à leur premier essai.
- a un **disque éphémère** : si tu redéploies (nouveau `git push`) ou si le
  service redémarre, les images uploadées par les utilisateurs (photos de
  pokémone, photos de post) sont perdues. Les comptes/textes restent (ils
  sont dans la base de données), mais pas les fichiers images. Pour un test
  entre amis de quelques jours, c'est un compromis raisonnable — je peux
  brancher un vrai stockage d'images plus tard si vous partez sur un
  vrai lancement.
- la base de données Postgres gratuite fournie **expire au bout de 30 jours**.
  Largement suffisant pour une phase de test.

---

## Étape 1 — Mettre le projet sur GitHub

Render déploie depuis un dépôt Git. Si tu n'as pas encore de compte GitHub,
crée-en un sur https://github.com (gratuit).

Dans PowerShell, à la racine du projet (`catchclub_django/`) :

```powershell
git init
git add .
git commit -m "CatchClub - premiere version"
```

Puis sur github.com : bouton **New repository**, nomme-le `catchclub`
(reste en **Private** si tu préfères, Render peut lire les dépôts privés),
ne coche aucune case d'initialisation, clique **Create repository**.

GitHub t'affiche ensuite des commandes à copier, du style :

```powershell
git remote add origin https://github.com/TON-PSEUDO/catchclub.git
git branch -M main
git push -u origin main
```

Colle-les dans PowerShell (Git te demandera de te connecter à GitHub la
première fois — suis les instructions à l'écran).

> Le dépôt fait ~95 Mo à cause des modèles 3D (`static/models/pokemon/`) :
> le push peut prendre quelques minutes selon ta connexion.

---

## Étape 2 — Déployer sur Render

1. Crée un compte sur https://render.com (tu peux t'inscrire directement
   avec ton compte GitHub, c'est le plus rapide).
2. Dans le tableau de bord Render : **New +** → **Blueprint**.
3. Connecte/choisis ton dépôt `catchclub`. Render détecte automatiquement
   le fichier `render.yaml` fourni dans le projet, qui décrit tout
   (site web + base de données Postgres gratuite).
4. Vérifie que les deux ressources proposées sont bien sur le plan
   **Free**, puis clique **Apply** / **Create**.
5. Render installe les dépendances, exécute les migrations et charge les
   données de démonstration automatiquement (`build.sh`). Ça prend
   quelques minutes la première fois — tu peux suivre la progression dans
   l'onglet **Logs**.
6. Une fois le déploiement terminé (statut **Live**), ton lien est affiché
   en haut de la page du service, du style :

   `https://catchclub.onrender.com`

C'est ce lien que tu envoies à tes amis. 🎉

---

## Étape 3 — Comptes pour tester

Les mêmes comptes de démo que sur ta machine (créés par `seed_demo`
pendant le build) :

| Rôle | Identifiant | Mot de passe |
|---|---|---|
| Administrateur | `admin` | `admin1234` |
| Modérateur (abonnements uniquement) | `modo` | `moderateur123` |
| Dresseurs | `Gilo`, `Aika`, `Ryu`, `Meji`, `Loran`, `MysteLia`, `Braisor_exe` | `motdepasse123` |

**Pense à changer ces mots de passe** (ou à créer de nouveaux comptes admin)
si le lien doit rester en ligne au-delà du test entre amis — tout le monde
peut lire ce README sur GitHub si le dépôt est public.

Tes amis peuvent bien sûr aussi créer leur propre compte et leur propre
pokémone directement depuis le site.

---

## Mettre à jour le site après une modification

Dès que tu veux pousser une nouvelle version :

```powershell
git add .
git commit -m "Description du changement"
git push
```

Render redéploie automatiquement à chaque `push` sur la branche `main`.
Rappel : ça remet à zéro le disque éphémère (voir l'avertissement en haut),
donc les images uploadées par les testeurs depuis la dernière fois seront
perdues — les comptes et les textes restent, eux, en sécurité dans la
base Postgres.

---

## Revenir en local après avoir testé en ligne

Ta copie locale n'est pas affectée par le déploiement : elle continue de
tourner sur SQLite (`python manage.py runserver`) sans rien changer. Les
deux environnements sont totalement indépendants.
