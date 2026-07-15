#!/usr/bin/env bash
# Script exécuté par Render à chaque déploiement.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Peuple le site avec les comptes de démonstration (admin, modo, dresseurs,
# groupes, posts...) au premier déploiement. Sans danger à relancer :
# la commande utilise get_or_create partout.
python manage.py seed_demo
